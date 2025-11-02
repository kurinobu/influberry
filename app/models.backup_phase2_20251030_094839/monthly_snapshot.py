# app/models/monthly_snapshot.py
"""
InfluBerry Monthly Snapshot モデル
月次スナップショット管理用データモデル
"""

from datetime import datetime
from app import db


class MonthlySnapshot(db.Model):
    """月次スナップショットモデル"""
    
    __tablename__ = 'monthly_snapshots'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Snapshot Information
    snapshot_month = db.Column(db.Date, nullable=False, index=True)  # スナップショット対象月（月初日）
    snapshot_data = db.Column(db.JSON, nullable=False)  # スナップショットデータ（JSON形式）
    
    # Metadata
    snapshot_type = db.Column(db.String(20), nullable=False, default='monthly')  # スナップショットタイプ
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'snapshot_month', 'snapshot_type', name='uq_user_snapshot_month_type'),
    )
    
    def __init__(self, user_id, snapshot_month, snapshot_data, snapshot_type='monthly'):
        """コンストラクタ"""
        self.user_id = user_id
        self.snapshot_month = snapshot_month
        self.snapshot_data = snapshot_data
        self.snapshot_type = snapshot_type
    
    def to_dict(self):
        """辞書形式でスナップショット情報を返す"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'snapshot_month': self.snapshot_month.isoformat() if self.snapshot_month else None,
            'snapshot_data': self.snapshot_data,
            'snapshot_type': self.snapshot_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def format_snapshot_month(self):
        """スナップショット対象月の日本語フォーマット"""
        if not self.snapshot_month:
            return None
        return f"{self.snapshot_month.year}年{self.snapshot_month.month}月"
    
    @classmethod
    def get_by_user_and_month(cls, user_id, year, month):
        """ユーザー・月別スナップショット取得"""
        target_date = datetime(year, month, 1).date()
        return cls.query.filter_by(
            user_id=user_id,
            snapshot_month=target_date,
            snapshot_type='monthly'
        ).first()
    
    @classmethod
    def get_by_user_and_date_range(cls, user_id, start_date, end_date):
        """ユーザー・期間別スナップショット取得"""
        return cls.query.filter(
            cls.user_id == user_id,
            cls.snapshot_month >= start_date,
            cls.snapshot_month <= end_date,
            cls.snapshot_type == 'monthly'
        ).order_by(cls.snapshot_month.desc()).all()
    
    @classmethod
    def create_snapshot(cls, user_id, year, month, stats_data, targets_data):
        """月次スナップショット作成"""
        snapshot_month = datetime(year, month, 1).date()
        
        # スナップショットデータの構築
        snapshot_data = {
            'stats': stats_data,
            'targets': targets_data,
            'snapshot_created_at': datetime.utcnow().isoformat(),
            'original_month': f"{year}-{month:02d}"
        }
        
        # 既存のスナップショットを削除（上書き）
        existing = cls.get_by_user_and_month(user_id, year, month)
        if existing:
            db.session.delete(existing)
        
        # 新しいスナップショットを作成
        snapshot = cls(
            user_id=user_id,
            snapshot_month=snapshot_month,
            snapshot_data=snapshot_data,
            snapshot_type='monthly'
        )
        
        db.session.add(snapshot)
        return snapshot
    
    @classmethod
    def get_latest_snapshots(cls, user_id, limit=3):
        """ユーザーの最新スナップショット取得（過去Nヶ月）"""
        return cls.query.filter_by(
            user_id=user_id,
            snapshot_type='monthly'
        ).order_by(cls.snapshot_month.desc()).limit(limit).all()
    
    def get_stats_data(self):
        """スナップショットから統計データを取得"""
        return self.snapshot_data.get('stats', {})
    
    def get_targets_data(self):
        """スナップショットから目標データを取得"""
        return self.snapshot_data.get('targets', {})
    
    def is_snapshot_valid(self):
        """スナップショットの有効性をチェック"""
        if not self.snapshot_data:
            return False
        
        required_keys = ['stats', 'targets', 'snapshot_created_at']
        return all(key in self.snapshot_data for key in required_keys)
