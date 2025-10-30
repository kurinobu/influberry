# app/models/monthly_summary.py
"""
InfluBerry Monthly Summary モデル
月次統計事前集計用データモデル（計画書v2.0準拠）
"""

from datetime import datetime
from app import db


class MonthlySummary(db.Model):
    """月次統計事前集計モデル"""
    
    __tablename__ = 'monthly_summary'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    summary_month = db.Column(db.Date, nullable=False, index=True)  # 対象月（月初日）
    
    # 案件関連（正負集計済み）
    acquired_projects = db.Column(db.Integer, default=0)  # 獲得案件数
    completed_projects = db.Column(db.Integer, default=0)  # 完了案件数
    
    # 請求書関連（会計ロジック準拠）
    sent_invoices_count = db.Column(db.Integer, default=0)  # 送信済み請求書件数
    sent_invoices_amount = db.Column(db.Numeric(12, 2), default=0)  # 送信済み金額
    paid_invoices_count = db.Column(db.Integer, default=0)  # 支払済み件数
    paid_invoices_amount = db.Column(db.Numeric(12, 2), default=0)  # 支払済み金額
    overdue_invoices_count = db.Column(db.Integer, default=0)  # 期限超過件数
    overdue_invoices_amount = db.Column(db.Numeric(12, 2), default=0)  # 期限超過金額
    
    # メタ情報
    last_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'summary_month', name='uq_user_summary_month'),
        db.Index('ix_monthly_summary_user_month', 'user_id', 'summary_month')
    )
    
    def __init__(self, user_id, summary_month, acquired_projects=0, completed_projects=0,
                 sent_invoices_count=0, sent_invoices_amount=0, paid_invoices_count=0,
                 paid_invoices_amount=0, overdue_invoices_count=0, overdue_invoices_amount=0):
        """コンストラクタ"""
        self.user_id = user_id
        self.summary_month = summary_month
        self.acquired_projects = acquired_projects
        self.completed_projects = completed_projects
        self.sent_invoices_count = sent_invoices_count
        self.sent_invoices_amount = sent_invoices_amount
        self.paid_invoices_count = paid_invoices_count
        self.paid_invoices_amount = paid_invoices_amount
        self.overdue_invoices_count = overdue_invoices_count
        self.overdue_invoices_amount = overdue_invoices_amount
    
    def to_dict(self):
        """辞書形式で統計情報を返す"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'summary_month': self.summary_month.isoformat() if self.summary_month else None,
            'acquired_projects': self.acquired_projects,
            'completed_projects': self.completed_projects,
            'sent_invoices_count': self.sent_invoices_count,
            'sent_invoices_amount': float(self.sent_invoices_amount),
            'paid_invoices_count': self.paid_invoices_count,
            'paid_invoices_amount': float(self.paid_invoices_amount),
            'overdue_invoices_count': self.overdue_invoices_count,
            'overdue_invoices_amount': float(self.overdue_invoices_amount),
            'last_updated_at': self.last_updated_at.isoformat() if self.last_updated_at else None
        }
    
    def update_stats(self, acquired_projects=None, completed_projects=None,
                    sent_invoices_count=None, sent_invoices_amount=None,
                    paid_invoices_count=None, paid_invoices_amount=None,
                    overdue_invoices_count=None, overdue_invoices_amount=None):
        """統計データを更新"""
        if acquired_projects is not None:
            self.acquired_projects = acquired_projects
        if completed_projects is not None:
            self.completed_projects = completed_projects
        if sent_invoices_count is not None:
            self.sent_invoices_count = sent_invoices_count
        if sent_invoices_amount is not None:
            self.sent_invoices_amount = sent_invoices_amount
        if paid_invoices_count is not None:
            self.paid_invoices_count = paid_invoices_count
        if paid_invoices_amount is not None:
            self.paid_invoices_amount = paid_invoices_amount
        if overdue_invoices_count is not None:
            self.overdue_invoices_count = overdue_invoices_count
        if overdue_invoices_amount is not None:
            self.overdue_invoices_amount = overdue_invoices_amount
        
        self.last_updated_at = datetime.utcnow()
    
    @classmethod
    def get_by_user_and_month(cls, user_id, summary_month):
        """ユーザー・月別統計取得"""
        return cls.query.filter_by(
            user_id=user_id,
            summary_month=summary_month
        ).first()
    
    @classmethod
    def get_by_user_and_year(cls, user_id, year):
        """ユーザー・年別統計取得"""
        from sqlalchemy import extract
        return cls.query.filter(
            cls.user_id == user_id,
            extract('year', cls.summary_month) == year
        ).order_by(cls.summary_month.asc()).all()
