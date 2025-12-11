"""
User model for InfluBerry v2
Flask-Login完全対応版 + TikTok OAuth対応
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """ユーザーモデル（Flask-Login対応 + TikTok OAuth対応）"""
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic User Information
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    influencer_name = db.Column(db.String(100), nullable=True)
    
    # TikTok OAuth用フィールド（新規追加）
    tiktok_id = db.Column(db.String(100), unique=True, nullable=True, index=True)
    tiktok_username = db.Column(db.String(100), nullable=True)
    tiktok_avatar_url = db.Column(db.String(500), nullable=True)
    oauth_provider = db.Column(db.String(20), nullable=True)  # 'email' or 'tiktok'
    
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
    # PDF印刷設定
    pdf_layout = db.Column(db.String(20), default='business', nullable=False)  # business, modern, classic
    pdf_paper_color = db.Column(db.String(7), default='#ffffff', nullable=False)  # HEXカラー
    pdf_font_family = db.Column(db.String(50), default='Noto Sans JP', nullable=False)  # フォント
    
    # 支払い情報設定（将来拡張対応: PayPay等の支払い方法追加可能）
    payment_method = db.Column(db.String(50), nullable=True)  # 銀行振込、PayPay等
    bank_name = db.Column(db.String(100), nullable=True)  # 銀行名
    branch_name = db.Column(db.String(100), nullable=True)  # 支店名
    account_type = db.Column(db.String(20), nullable=True)  # 普通、当座
    account_number = db.Column(db.String(20), nullable=True)  # 口座番号
    account_holder = db.Column(db.String(100), nullable=True)  # 口座名義
    
    # 請求者情報設定（PDF出力用）
    issuer_name = db.Column(db.String(100), nullable=False, default='')  # 請求者名（必須）
    office_address = db.Column(db.String(200), nullable=True)  # オフィス所在地（任意）
    contact_info = db.Column(db.String(100), nullable=True)  # 連絡先（任意）
    
    projects = db.relationship('Project', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password=None, influencer_name=None, **kwargs):
        """ユーザー初期化（TikTok OAuth対応）"""
        self.username = username
        self.email = email
        
        # パスワードはTikTokログイン時はNoneの場合がある
        if password:
            self.set_password(password)
        else:
            # TikTokログイン時はダミーパスワードを設定（ログインには使用されない）
            self.password_hash = generate_password_hash('OAUTH_USER_NO_PASSWORD')
        
        self.influencer_name = influencer_name
        self.is_active = kwargs.get('is_active', True)
        self.plan_type = kwargs.get('plan_type', 'free')
        
        # TikTok OAuth情報の設定
        self.tiktok_id = kwargs.get('tiktok_id')
        self.tiktok_username = kwargs.get('tiktok_username')
        self.tiktok_avatar_url = kwargs.get('tiktok_avatar_url')
        self.oauth_provider = kwargs.get('oauth_provider', 'email')
    
    def set_password(self, password):
        """パスワードハッシュ化"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """パスワード検証"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """ユーザー情報を辞書形式で返す（TikTok情報含む）"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'influencer_name': self.influencer_name,
            'issuer_name': self.issuer_name,
            'office_address': self.office_address,
            'contact_info': self.contact_info,
            'is_active': self.is_active,
            'plan_type': self.plan_type,
            'oauth_provider': self.oauth_provider,
            'tiktok_username': self.tiktok_username,
            'tiktok_avatar_url': self.tiktok_avatar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def create(cls, username, email, password=None, influencer_name=None, **kwargs):
        """ユーザー作成クラスメソッド（TikTok OAuth対応）"""
        user = cls(username, email, password, influencer_name, **kwargs)
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def create_from_tiktok(cls, tiktok_id, tiktok_username, tiktok_avatar_url):
        """TikTokユーザーからアカウント作成"""
        # 一意なユーザー名生成（tiktok_id の最初の8文字を使用）
        username = f"tiktok_{tiktok_id[:8]}"
        
        # メールアドレスは必須だが、TikTokは提供しないのでダミーを使用
        email = f"{username}@tiktok.influberry.local"
        
        user = cls(
            username=username,
            email=email,
            password=None,  # パスワード不要（OAuth認証）
            influencer_name=tiktok_username,
            tiktok_id=tiktok_id,
            tiktok_username=tiktok_username,
            tiktok_avatar_url=tiktok_avatar_url,
            oauth_provider='tiktok'
        )
        
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