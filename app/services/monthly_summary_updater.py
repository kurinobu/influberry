# app/services/monthly_summary_updater.py
"""
月次統計事前集計更新サービス
計画書v2.0準拠: ステータス変更時の自動更新機能
"""

from app import db
from app.models.monthly_summary import MonthlySummary
from app.models.project import Project
from app.models.invoice import Invoice
from app.models.project_status_history import ProjectStatusHistory
from app.models.invoice_status_history import InvoiceStatusHistory
from sqlalchemy import extract, func
from datetime import datetime, date


def update_monthly_summary(user_id, changed_month):
    """
    月次サマリーを再計算・更新
    ステータス変更時に呼び出される
    
    Args:
        user_id (int): ユーザーID
        changed_month (datetime): 変更が発生した月（月初日）
    """
    year = changed_month.year
    month = changed_month.month
    
    print(f"🔧 月次サマリー更新開始: user_id={user_id}, month={year}-{month:02d}")
    
    # 正負集計（計画書v2.0準拠）
    acquired = _calculate_acquired_projects(user_id, year, month)
    completed = _calculate_completed_projects(user_id, year, month)
    sent_count, sent_amount = _calculate_sent_invoices(user_id, year, month)
    paid_count, paid_amount = _calculate_paid_invoices(user_id, year, month)
    overdue_count, overdue_amount = _calculate_overdue_invoices(user_id, year, month)
    
    # UPSERT
    summary = MonthlySummary.query.filter_by(
        user_id=user_id,
        summary_month=changed_month.date()
    ).first()
    
    if summary:
        # 既存レコードを更新
        summary.update_stats(
            acquired_projects=acquired,
            completed_projects=completed,
            sent_invoices_count=sent_count,
            sent_invoices_amount=sent_amount,
            paid_invoices_count=paid_count,
            paid_invoices_amount=paid_amount,
            overdue_invoices_count=overdue_count,
            overdue_invoices_amount=overdue_amount
        )
        print(f"✅ 月次サマリー更新完了: 既存レコード更新")
    else:
        # 新規レコード作成
        summary = MonthlySummary(
            user_id=user_id,
            summary_month=changed_month.date(),
            acquired_projects=acquired,
            completed_projects=completed,
            sent_invoices_count=sent_count,
            sent_invoices_amount=sent_amount,
            paid_invoices_count=paid_count,
            paid_invoices_amount=paid_amount,
            overdue_invoices_count=overdue_count,
            overdue_invoices_amount=overdue_amount
        )
        db.session.add(summary)
        print(f"✅ 月次サマリー更新完了: 新規レコード作成")
    
    db.session.commit()
    print(f"✅ 月次サマリー更新完了: user_id={user_id}, month={year}-{month:02d}")


def _calculate_acquired_projects(user_id, year, month):
    """獲得案件数の正負集計（計画書v2.0準拠）
    最適化: extract()関数を使わず、日付範囲でのフィルタリングによりインデックスを有効活用
    """
    # 日付範囲を計算（インデックスを有効活用するため）
    month_start = datetime(year, month, 1)
    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)
    
    # 正の変化（proposed → contracted: +1）
    positive = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'proposed',
        ProjectStatusHistory.new_status == 'contracted',
        ProjectStatusHistory.changed_at >= month_start,
        ProjectStatusHistory.changed_at < month_end
    ).scalar() or 0
    
    # 負の変化（contracted → proposed: -1）
    negative = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'contracted',
        ProjectStatusHistory.new_status == 'proposed',
        ProjectStatusHistory.changed_at >= month_start,
        ProjectStatusHistory.changed_at < month_end
    ).scalar() or 0
    
    return positive - negative


def _calculate_completed_projects(user_id, year, month):
    """完了案件数の正負集計（計画書v2.0準拠）
    最適化: extract()関数を使わず、日付範囲でのフィルタリングによりインデックスを有効活用
    """
    # 日付範囲を計算（インデックスを有効活用するため）
    month_start = datetime(year, month, 1)
    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)
    
    # 正の変化（contracted → completed: +1）
    positive = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'contracted',
        ProjectStatusHistory.new_status == 'completed',
        ProjectStatusHistory.changed_at >= month_start,
        ProjectStatusHistory.changed_at < month_end
    ).scalar() or 0
    
    # 負の変化（completed → contracted: -1）
    negative = db.session.query(
        func.count(func.distinct(ProjectStatusHistory.project_id))
    ).join(Project).filter(
        Project.user_id == user_id,
        ProjectStatusHistory.old_status == 'completed',
        ProjectStatusHistory.new_status == 'contracted',
        ProjectStatusHistory.changed_at >= month_start,
        ProjectStatusHistory.changed_at < month_end
    ).scalar() or 0
    
    return positive - negative


def _calculate_sent_invoices(user_id, year, month):
    """送信済み請求書の集計（会計ロジック準拠）
    最適化: extract()関数を使わず、日付範囲でのフィルタリングによりインデックスを有効活用
    """
    # 日付範囲を計算（インデックスを有効活用するため）
    month_start = datetime(year, month, 1)
    if month == 12:
        month_end = datetime(year + 1, 1, 1)
    else:
        month_end = datetime(year, month + 1, 1)
    
    # 正の変化（draft → sent: +金額）
    positive = db.session.query(
        func.count(func.distinct(InvoiceStatusHistory.invoice_id)),
        func.sum(Invoice.total_amount)
    ).join(Invoice).filter(
        Invoice.user_id == user_id,
        InvoiceStatusHistory.old_status == 'draft',
        InvoiceStatusHistory.new_status == 'sent',
        InvoiceStatusHistory.changed_at >= month_start,
        InvoiceStatusHistory.changed_at < month_end
    ).first()
    
    # 負の変化（sent → draft/canceled: -金額）
    negative = db.session.query(
        func.count(func.distinct(InvoiceStatusHistory.invoice_id)),
        func.sum(Invoice.total_amount)
    ).join(Invoice).filter(
        Invoice.user_id == user_id,
        InvoiceStatusHistory.old_status == 'sent',
        InvoiceStatusHistory.new_status.in_(['draft', 'canceled']),
        InvoiceStatusHistory.changed_at >= month_start,
        InvoiceStatusHistory.changed_at < month_end
    ).first()
    
    count = (positive[0] or 0) - (negative[0] or 0)
    amount = float(positive[1] or 0) - float(negative[1] or 0)
    
    return count, amount


def _calculate_paid_invoices(user_id, year, month):
    """支払済み請求書の集計（payment_date基準）
    最適化: extract()関数を使わず、日付範囲でのフィルタリングによりインデックスを有効活用
    """
    # payment_dateはDATE型のため、date型で範囲を計算
    payment_month_start = date(year, month, 1)
    if month == 12:
        payment_month_end = date(year + 1, 1, 1)
    else:
        payment_month_end = date(year, month + 1, 1)
    
    result = db.session.query(
        func.count(Invoice.id),
        func.sum(Invoice.total_amount)
    ).filter(
        Invoice.user_id == user_id,
        Invoice.status == 'paid',
        Invoice.payment_date.isnot(None),
        Invoice.payment_date >= payment_month_start,
        Invoice.payment_date < payment_month_end
    ).first()
    
    count = result[0] or 0
    amount = float(result[1] or 0)
    
    return count, amount


def _calculate_overdue_invoices(user_id, year, month):
    """期限超過請求書の集計"""
    # 現在は簡易実装（将来拡張予定）
    # TODO: 期限超過ロジックの実装
    return 0, 0.0


def recalculate_all_monthly_summaries(user_id):
    """
    指定ユーザーの全月次サマリーを再計算
    データ整合性チェック用
    """
    print(f"🔧 全月次サマリー再計算開始: user_id={user_id}")
    
    # ユーザーの全月次サマリーを取得
    summaries = MonthlySummary.query.filter_by(user_id=user_id).all()
    
    for summary in summaries:
        changed_month = datetime.combine(summary.summary_month, datetime.min.time())
        update_monthly_summary(user_id, changed_month)
    
    print(f"✅ 全月次サマリー再計算完了: user_id={user_id}")
