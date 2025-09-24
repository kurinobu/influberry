# app/models/project.py
"""
InfluBerry Project モデル
スポンサー案件管理用データモデル
"""

from datetime import datetime, date, timedelta
from decimal import Decimal
from app import db


class Project(db.Model):
    """スポンサー案件管理モデル"""
    
    __tablename__ = 'projects'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Project Information
    company_name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # 金額（最大8桁、小数点2桁）
    deadline = db.Column(db.Date, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    
    # Project Status
    status = db.Column(
        db.String(20), 
        nullable=False, 
        default='proposed',
        index=True
    )
    # Status options: 'proposed', 'contracted', 'completed'

    # New extensible fields (拡張可能フィールド)
    project_name = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    # BerryDo Todo拡張フィールド（PostgreSQLスキーマと整合）
    is_todo = db.Column(db.Boolean, default=False, nullable=True)
    todo_title = db.Column(db.String(255), nullable=True)
    todo_description = db.Column(db.Text, nullable=True)
    todo_due_date = db.Column(db.Date, nullable=True)
    todo_priority = db.Column(db.String(10), nullable=True)
    todo_importance = db.Column(db.Integer, nullable=True)
    todo_status = db.Column(db.String(20), nullable=True)
    
    def __init__(self, **kwargs):
        """Project初期化メソッド - Todo拡張フィールド対応"""
        super(Project, self).__init__(**kwargs)
        
        # Todo拡張フィールドの明示的設定
        if 'is_todo' in kwargs:
            self.is_todo = kwargs['is_todo']
        if 'todo_title' in kwargs:
            self.todo_title = kwargs['todo_title']
        if 'todo_description' in kwargs:
            self.todo_description = kwargs['todo_description']
        if 'todo_priority' in kwargs:
            self.todo_priority = kwargs['todo_priority']
        if 'todo_importance' in kwargs:
            self.todo_importance = kwargs['todo_importance']
        if 'todo_status' in kwargs:
            self.todo_status = kwargs['todo_status']

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __init__(self, user_id, company_name, amount, deadline, description, **kwargs):
        """コンストラクタ"""
        self.user_id = user_id
        self.company_name = company_name
        self.amount = Decimal(str(amount))  # Decimal型で精度保証
        self.deadline = deadline if isinstance(deadline, date) else datetime.strptime(deadline, '%Y-%m-%d').date()
        self.description = description
        
        # 新フィールド追加
        self.project_name = kwargs.get('project_name', company_name)  # デフォルト値で安全性確保
        self.notes = kwargs.get('notes', '')
        
        # オプション引数
        self.status = kwargs.get('status', 'proposed')
    
    def to_dict(self):
        """辞書形式でプロジェクト情報を返す"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'project_name': self.project_name,  # 新フィールド追加
            'amount': float(self.amount) if self.amount else 0.0,
            'amount_formatted': self.format_amount(),
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'deadline_formatted': self.format_deadline(),
            'description': self.description,
            'notes': self.notes,  # 新フィールド追加
            'status': self.status,
            'status_display': self.get_status_display(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_overdue': self.is_overdue(),
            'days_until_deadline': self.days_until_deadline()
        }
    
    def format_amount(self):
        """金額の日本語フォーマット"""
        if not self.amount:
            return "¥0"
        return f"¥{self.amount:,.0f}"
    
    def format_deadline(self):
        """納期の日本語フォーマット"""
        if not self.deadline:
            return ""
        return self.deadline.strftime('%Y年%m月%d日')
    
    def get_status_display(self):
        """ステータスの日本語表示"""
        status_map = {
            'proposed': '提案中',
            'contracted': '契約中', 
            'completed': '完了'
        }
        return status_map.get(self.status, self.status)
    
    def is_overdue(self):
        """納期を過ぎているかチェック"""
        if not self.deadline or self.status == 'completed':
            return False
        return date.today() > self.deadline
    
    def days_until_deadline(self):
        """納期までの残り日数"""
        if not self.deadline or self.status == 'completed':
            return None
        
        delta = self.deadline - date.today()
        return delta.days
    
    def update_status(self, new_status):
        """ステータス更新"""
        valid_statuses = ['proposed', 'contracted', 'completed']
        if new_status not in valid_statuses:
            raise ValueError(f"無効なステータス: {new_status}. 有効な値: {valid_statuses}")
        
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def can_edit(self):
        """編集可能かチェック"""
        return self.status != 'completed'
    
    def can_delete(self):
        """削除可能かチェック"""
        return self.status == 'proposed'
    
    @classmethod
    def get_by_user(cls, user_id, status=None):
        """ユーザー別案件取得"""
        query = cls.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(cls.deadline.asc(), cls.created_at.desc()).all()
    
    @classmethod
    def get_overdue_projects(cls, user_id):
        """期限切れ案件取得"""
        return cls.query.filter(
            cls.user_id == user_id,
            cls.deadline < date.today(),
            cls.status.in_(['proposed', 'contracted'])
        ).order_by(cls.deadline.asc()).all()
    
    @classmethod
    def get_upcoming_deadlines(cls, user_id, days=7):
        """近日中の納期案件取得"""
        upcoming_date = date.today() + timedelta(days=days)
        return cls.query.filter(
            cls.user_id == user_id,
            cls.deadline <= upcoming_date,
            cls.deadline >= date.today(),
            cls.status.in_(['proposed', 'contracted'])
        ).order_by(cls.deadline.asc()).all()
    
    def __repr__(self):
        """文字列表現"""
        return f'<Project {self.company_name} - {self.status}>'