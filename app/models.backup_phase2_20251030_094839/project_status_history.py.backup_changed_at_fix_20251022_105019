# app/models/project_status_history.py
"""
InfluBerry Project Status History モデル
案件ステータス変更履歴管理用データモデル
"""

from datetime import datetime
from app import db


class ProjectStatusHistory(db.Model):
    """案件ステータス変更履歴モデル"""
    
    __tablename__ = 'project_status_history'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
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
            "new_status IN ('proposed', 'contracted', 'completed')",
            name='ck_project_status_history_new_status'
        ),
    )
    
    def __init__(self, project_id, old_status=None, new_status=None, changed_by=None, notes=None):
        """コンストラクタ"""
        self.project_id = project_id
        self.old_status = old_status
        self.new_status = new_status
        self.changed_by = changed_by
        self.notes = notes
    
    def to_dict(self):
        """辞書形式で履歴情報を返す"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'old_status': self.old_status,
            'new_status': self.new_status,
            'changed_by': self.changed_by,
            'notes': self.notes,
            'changed_at': self.changed_at.isoformat() if self.changed_at else None
        }
    
    def get_status_display(self, status):
        """ステータスの日本語表示"""
        status_map = {
            'proposed': '提案中',
            'contracted': '契約中',
            'completed': '完了'
        }
        return status_map.get(status, status)
    
    def get_old_status_display(self):
        """変更前ステータスの日本語表示"""
        return self.get_status_display(self.old_status) if self.old_status else '新規'
    
    def get_new_status_display(self):
        """変更後ステータスの日本語表示"""
        return self.get_status_display(self.new_status)
    
    @classmethod
    def get_by_project(cls, project_id):
        """案件別履歴取得"""
        return cls.query.filter_by(project_id=project_id).order_by(cls.changed_at.asc()).all()
    
    @classmethod
    def get_by_user_and_month(cls, user_id, year, month):
        """ユーザー・月別履歴取得"""
        from app.models.project import Project
        
        return cls.query.join(Project).filter(
            Project.user_id == user_id,
            db.extract('year', cls.changed_at) == year,
            db.extract('month', cls.changed_at) == month
        ).order_by(cls.changed_at.desc()).all()
    
    @classmethod
    def get_status_changes_by_month(cls, user_id, year, month, status):
        """特定ステータスへの変更を月別で取得"""
        from app.models.project import Project
        
        return cls.query.join(Project).filter(
            Project.user_id == user_id,
            cls.new_status == status,
            db.extract('year', cls.changed_at) == year,
            db.extract('month', cls.changed_at) == month
        ).all()
    
    def __repr__(self):
        """文字列表現"""
        return f'<ProjectStatusHistory {self.id}: project_id={self.project_id}, {self.old_status} -> {self.new_status}>'
