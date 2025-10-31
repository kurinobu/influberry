"""
月次管理API - 統合エンドポイント
計画書v2.0準拠: /api/monthly/current 実装
目的: 3ヶ月分のデータを1回のリクエストで返す（高速化）

Phase 1: 正式版として登録
- monthly_summaryテーブル対応
- 既存APIとの統合
- パフォーマンス最適化
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import extract, func
from app import db
from app.models.monthly_target import MonthlyTarget
from app.models.monthly_summary import MonthlySummary
from app.models.project import Project
from app.models.invoice import Invoice
from app.models.project_status_history import ProjectStatusHistory
from app.models.invoice_status_history import InvoiceStatusHistory

monthly_current_bp = Blueprint('monthly_current', __name__)


def get_three_months():
    """
    今月+先月+次月の3ヶ月を取得
    """
    now = datetime.now()
    current_month = datetime(now.year, now.month, 1)
    last_month = current_month - timedelta(days=1)
    last_month = datetime(last_month.year, last_month.month, 1)
    
    next_month_date = current_month + timedelta(days=32)
    next_month = datetime(next_month_date.year, next_month_date.month, 1)
    
    return {
        'last': last_month,
        'current': current_month,
        'next': next_month
    }


def calculate_monthly_stats(user_id, year, month):
    """
    月次統計を計算（正負集計ロジック対応）
    """
    # 獲得案件数（proposed → contracted）
    acquired_positive = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'proposed',
        ProjectStatusHistory.new_status == 'contracted',
        extract('year', ProjectStatusHistory.changed_at) == year,
        extract('month', ProjectStatusHistory.changed_at) == month
    ).scalar() or 0
    
    # 獲得案件数の負（contracted → proposed）
    acquired_negative = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'contracted',
        ProjectStatusHistory.new_status == 'proposed',
        extract('year', ProjectStatusHistory.changed_at) == year,
        extract('month', ProjectStatusHistory.changed_at) == month
    ).scalar() or 0
    
    acquired_projects = acquired_positive - acquired_negative
    
    # 完了案件数（contracted → completed）
    completed_positive = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'contracted',
        ProjectStatusHistory.new_status == 'completed',
        extract('year', ProjectStatusHistory.changed_at) == year,
        extract('month', ProjectStatusHistory.changed_at) == month
    ).scalar() or 0
    
    # 完了案件数の負（completed → contracted）
    completed_negative = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'completed',
        ProjectStatusHistory.new_status == 'contracted',
        extract('year', ProjectStatusHistory.changed_at) == year,
        extract('month', ProjectStatusHistory.changed_at) == month
    ).scalar() or 0
    
    completed_projects = completed_positive - completed_negative
    
    # 送信済み請求書（draft → sent）
    sent_positive = db.session.query(
        func.count(func.distinct(InvoiceStatusHistory.invoice_id)),
        func.sum(Invoice.total_amount)
    ).join(Invoice).filter(
        Invoice.user_id == user_id,
        InvoiceStatusHistory.old_status == 'draft',
        InvoiceStatusHistory.new_status == 'sent',
        extract('year', InvoiceStatusHistory.changed_at) == year,
        extract('month', InvoiceStatusHistory.changed_at) == month
    ).first()
    
    # 送信済み請求書の負（sent → draft/canceled）
    sent_negative = db.session.query(
        func.count(func.distinct(InvoiceStatusHistory.invoice_id)),
        func.sum(Invoice.total_amount)
    ).join(Invoice).filter(
        Invoice.user_id == user_id,
        InvoiceStatusHistory.old_status == 'sent',
        InvoiceStatusHistory.new_status.in_(['draft', 'canceled']),
        extract('year', InvoiceStatusHistory.changed_at) == year,
        extract('month', InvoiceStatusHistory.changed_at) == month
    ).first()
    
    sent_count = (sent_positive[0] or 0) - (sent_negative[0] or 0)
    sent_amount = float(sent_positive[1] or 0) - float(sent_negative[1] or 0)
    
    # 支払済み請求書（payment_date基準）
    paid_result = db.session.query(
        func.count(Invoice.id),
        func.sum(Invoice.total_amount)
    ).filter(
        Invoice.user_id == user_id,
        Invoice.status == 'paid',
        Invoice.payment_date.isnot(None),
        extract('year', Invoice.payment_date) == year,
        extract('month', Invoice.payment_date) == month
    ).first()
    
    paid_count = paid_result[0] or 0
    paid_amount = float(paid_result[1] or 0)
    
    return {
        'acquired_projects': acquired_projects,
        'completed_projects': completed_projects,
        'sent_invoices_count': sent_count,
        'sent_invoices_amount': sent_amount,
        'paid_invoices_count': paid_count,
        'paid_invoices_amount': paid_amount
    }


@monthly_current_bp.route('/api/monthly/current', methods=['GET'])
@login_required
def get_current_monthly_data():
    """
    現在の月次データ取得（今月+先月+次月）
    計画書v2.0準拠: 認証方式を既存APIと統一（Flask-Login使用）
    
    レスポンス形式:
    {
        "success": true,
        "current_month": "2025-10-01",
        "data": {
            "2025-09-01": {
                "target": { "projects": 5, "income": 200000 },
                "stats": { "acquired_projects": 3, ... }
            },
            "2025-10-01": { ... },
            "2025-11-01": { ... }
        }
    }
    """
    try:
        user_id = current_user.id
        months = get_three_months()
        
        result = {
            'success': True,
            'current_month': months['current'].strftime('%Y-%m-01'),
            'data': {}
        }
        
        # 3ヶ月分のデータを取得
        for key, month_date in months.items():
            month_key = month_date.strftime('%Y-%m-01')
            
            # 目標取得
            target = MonthlyTarget.query.filter_by(
                user_id=user_id,
                target_month=month_date
            ).first()
            
            # 統計取得（事前集計テーブル優先）
            summary = MonthlySummary.get_by_user_and_month(user_id, month_date.date())
            if summary:
                # 事前集計テーブルから高速取得
                stats = {
                    'acquired_projects': summary.acquired_projects,
                    'completed_projects': summary.completed_projects,
                    'sent_invoices_count': summary.sent_invoices_count,
                    'sent_invoices_amount': float(summary.sent_invoices_amount),
                    'paid_invoices_count': summary.paid_invoices_count,
                    'paid_invoices_amount': float(summary.paid_invoices_amount),
                    'overdue_invoices_count': summary.overdue_invoices_count,
                    'overdue_invoices_amount': float(summary.overdue_invoices_amount)
                }
            else:
                # フォールバック: リアルタイム計算
                stats = calculate_monthly_stats(
                    user_id,
                    month_date.year,
                    month_date.month
                )
            
            # データ統合
            result['data'][month_key] = {
                'target': {
                    'projects': target.target_projects if target else None,
                    'income': target.target_income if target else None
                },
                'stats': stats,
                'achievement': {
                    'projects_rate': (
                        stats['acquired_projects'] / target.target_projects
                        if target and target.target_projects
                        else 0
                    ),
                    'income_rate': (
                        stats['sent_invoices_amount'] / target.target_income
                        if target and target.target_income
                        else 0
                    )
                }
            }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500