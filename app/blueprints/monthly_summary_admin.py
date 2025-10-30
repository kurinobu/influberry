# app/blueprints/monthly_summary_admin.py
"""
月次サマリー管理API
計画書v2.0準拠: 手動更新・データ整合性チェック用
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.models.monthly_summary import MonthlySummary
from app.services.monthly_summary_updater import update_monthly_summary, recalculate_all_monthly_summaries

monthly_summary_admin_bp = Blueprint('monthly_summary_admin', __name__)


@monthly_summary_admin_bp.route('/api/monthly-summary/update', methods=['POST'])
@login_required
def manual_update_summary():
    """
    手動で月次サマリーを更新
    データ整合性チェック用
    """
    try:
        data = request.get_json()
        target_month = data.get('target_month')  # '2025-10-01'形式
        
        if not target_month:
            return jsonify({
                'success': False,
                'error': 'target_monthが必要です'
            }), 400
        
        # 日付パース
        try:
            target_date = datetime.strptime(target_month, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'target_monthの形式が正しくありません（YYYY-MM-DD）'
            }), 400
        
        # 月次サマリー更新
        update_monthly_summary(current_user.id, target_date)
        
        return jsonify({
            'success': True,
            'message': f'月次サマリーを更新しました: {target_month}',
            'target_month': target_month
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'月次サマリー更新エラー: {str(e)}'
        }), 500


@monthly_summary_admin_bp.route('/api/monthly-summary/recalculate-all', methods=['POST'])
@login_required
def recalculate_all():
    """
    全月次サマリーを再計算
    データ整合性チェック用
    """
    try:
        recalculate_all_monthly_summaries(current_user.id)
        
        return jsonify({
            'success': True,
            'message': '全月次サマリーの再計算が完了しました'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'全月次サマリー再計算エラー: {str(e)}'
        }), 500


@monthly_summary_admin_bp.route('/api/monthly-summary/status', methods=['GET'])
@login_required
def get_summary_status():
    """
    月次サマリーの状態確認
    デバッグ用
    """
    try:
        # 過去6ヶ月のサマリー状態を取得
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        six_months_ago = six_months_ago.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        summaries = MonthlySummary.query.filter(
            MonthlySummary.user_id == current_user.id,
            MonthlySummary.summary_month >= six_months_ago.date()
        ).order_by(MonthlySummary.summary_month.desc()).all()
        
        result = []
        for summary in summaries:
            result.append({
                'month': summary.summary_month.isoformat(),
                'acquired_projects': summary.acquired_projects,
                'completed_projects': summary.completed_projects,
                'sent_invoices_count': summary.sent_invoices_count,
                'sent_invoices_amount': float(summary.sent_invoices_amount),
                'paid_invoices_count': summary.paid_invoices_count,
                'paid_invoices_amount': float(summary.paid_invoices_amount),
                'last_updated_at': summary.last_updated_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'月次サマリー状態取得エラー: {str(e)}'
        }), 500
