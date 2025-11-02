# app/models/invoice_status_history.py
"""
InfluBerry Invoice Status History モデル
請求書ステータス変更履歴管理用データモデル
"""

from datetime import datetime
from app import db


class InvoiceStatusHistory(db.Model):
    """請求書ステータス変更履歴モデル"""
    
    __tablename__ = 'invoice_status_history'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id', ondelete='CASCADE'), nullable=False, index=True)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Status Information
    old_status = db.Column(db.String(20), nullable=True)  # 変更前ステータス（初回はNULL）
    new_status = db.Column(db.String(20), nullable=False)  # 変更後ステータス
    notes = db.Column(db.Text, nullable=True)  # 変更理由等（オプション）
    
    # Timestamp
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Status validation
    __table_args__ = (
        db.CheckConstraint(
            "new_status IN ('draft', 'sent', 'paid', 'canceled', 'overdue')",
            name='ck_invoice_status_history_new_status'
        ),
    )
    
    def __init__(self, invoice_id, old_status=None, new_status=None, changed_by=None, notes=None):
        """コンストラクタ"""
        self.invoice_id = invoice_id
        self.old_status = old_status
        self.new_status = new_status
        self.changed_by = changed_by
        self.notes = notes
    
    def to_dict(self):
        """辞書形式で履歴情報を返す"""
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'old_status': self.old_status,
            'new_status': self.new_status,
            'changed_by': self.changed_by,
            'notes': self.notes,
            'changed_at': self.changed_at.isoformat() if self.changed_at else None
        }
    
    def get_status_display(self, status):
        """ステータスの日本語表示"""
        status_map = {
            'draft': '下書き',
            'sent': '送信済',
            'paid': '支払済',
            'canceled': 'キャンセル',
            'overdue': '期限切れ'
        }
        return status_map.get(status, status)
    
    def get_old_status_display(self):
        """変更前ステータスの日本語表示"""
        return self.get_status_display(self.old_status) if self.old_status else '新規'
    
    def get_new_status_display(self):
        """変更後ステータスの日本語表示"""
        return self.get_status_display(self.new_status)
    
    @classmethod
    def get_by_invoice(cls, invoice_id):
        """請求書別履歴取得"""
        return cls.query.filter_by(invoice_id=invoice_id).order_by(cls.changed_at.asc()).all()
    
    @classmethod
    def get_by_user_and_month(cls, user_id, year, month):
        """ユーザー・月別履歴取得"""
        from app.models.invoice import Invoice
        
        return cls.query.join(Invoice).filter(
            Invoice.user_id == user_id,
            db.extract('year', cls.changed_at) == year,
            db.extract('month', cls.changed_at) == month
        ).order_by(cls.changed_at.desc()).all()
    
    @classmethod
    def get_status_changes_by_month(cls, user_id, year, month, status):
        """特定ステータスへの変更を月別で取得"""
        from app.models.invoice import Invoice
        
        return cls.query.join(Invoice).filter(
            Invoice.user_id == user_id,
            cls.new_status == status,
            db.extract('year', cls.changed_at) == year,
            db.extract('month', cls.changed_at) == month
        ).all()
    
    def __repr__(self):
        """文字列表現"""
        return f'<InvoiceStatusHistory {self.id}: invoice_id={self.invoice_id}, {self.old_status} -> {self.new_status}>'
