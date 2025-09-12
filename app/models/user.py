"""
User model for InfluBerry v2
Flask-Login完全対応版
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """ユーザーモデル（Flask-Login対応）"""
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic User Information
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    influencer_name = db.Column(db.String(100), nullable=True)
    
    # User Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    plan_type = db.Column(db.String(20), default='free', nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    
    # Relationships
    projects = db.relationship('Project', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, influencer_name=None, **kwargs):
        """ユーザー初期化"""
        self.username = username
        self.email = email
        self.set_password(password)
        self.influencer_name = influencer_name
        self.is_active = kwargs.get('is_active', True)
        self.plan_type = kwargs.get('plan_type', 'free')
    
    def set_password(self, password):
        """パスワードハッシュ化"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """パスワード検証"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """辞書形式変換"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'influencer_name': self.influencer_name,
            'is_active': self.is_active,
            'plan_type': self.plan_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    
    
    @classmethod
    def create(cls, username, email, password, influencer_name=None, **kwargs):
        """ユーザー作成クラスメソッド"""
        user = cls(username, email, password, influencer_name, **kwargs)
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update(self, **kwargs):
        """ユーザー情報更新"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'id':
                if key == 'password':
                    self.set_password(value)
                else:
                    setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """ユーザー削除"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def __repr__(self):
        return f'<User {self.username}>'