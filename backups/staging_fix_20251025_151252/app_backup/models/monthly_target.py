# app/models/monthly_target.py
"""
InfluBerry Monthly Target モデル
月次目標管理用データモデル
"""

from datetime import datetime
from app import db


class MonthlyTarget(db.Model):
    """月次目標管理モデル"""
    
    __tablename__ = 'monthly_targets'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Target Information
    target_month = db.Column(db.Date, nullable=False, index=True)  # 対象月（月初日）
    target_projects = db.Column(db.Integer, nullable=True)  # 目標案件数
    target_income = db.Column(db.Integer, nullable=True)    # 目標報酬額（円）
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'target_month', name='uq_user_target_month'),
    )
    
    def __init__(self, user_id, target_month, target_projects=None, target_income=None):
        """コンストラクタ"""
        self.user_id = user_id
        self.target_month = target_month
        self.target_projects = target_projects
        self.target_income = target_income
    
    def to_dict(self):
        """辞書形式で目標情報を返す"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_month': self.target_month.isoformat() if self.target_month else None,
            'target_projects': self.target_projects,
            'target_income': self.target_income,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def format_target_month(self):
        """対象月の日本語フォーマット"""
        if not self.target_month:
            return ""
        return self.target_month.strftime('%Y年%m月')
    
    def format_target_income(self):
        """目標報酬額の日本語フォーマット"""
        if not self.target_income:
            return "¥0"
        return f"¥{self.target_income:,}"
    
    @classmethod
    def get_by_user_and_month(cls, user_id, target_month):
        """ユーザー・月別目標取得"""
        return cls.query.filter_by(
            user_id=user_id,
            target_month=target_month
        ).first()
    
    @classmethod
    def get_by_user_and_year(cls, user_id, year):
        """ユーザー・年別目標一覧取得"""
        return cls.query.filter(
            cls.user_id == user_id,
            db.extract('year', cls.target_month) == year
        ).order_by(cls.target_month.asc()).all()
    
    def __repr__(self):
        """文字列表現"""
        return f'<MonthlyTarget {self.id}: user_id={self.user_id}, month={self.target_month}>'
