"""
Flask application configuration
InfluBerry v2 - シンプル構成版
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# .envファイル読み込み
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Core Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'influberry-secret-key-2025-change-in-production'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/influberry_dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login Configuration  
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    SESSION_PROTECTION = 'basic'
    
    # CORS Configuration
    # REST API CORS Configuration (Backend分離対応)
    CORS_ORIGINS = [
        os.environ.get('FRONTEND_URL', 'http://localhost:3000'),
        'http://localhost:5001',
        'http://localhost:5173',
        'http://localhost:5174',
        'http://127.0.0.1:5001',
        'http://127.0.0.1:5173',
        # 本番環境用（将来追加）
        'https://influberry.jp',
        'https://app.influberry.jp'
    ]
    
    # Development Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', '0').lower() in ['1', 'true', 'on']
    TESTING = False
    
    # Rate Limiting (Flask-Limiter)
    RATELIMIT_STORAGE_URI = 'memory://'
    RATELIMIT_DEFAULT = '100 per hour'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # SQL文出力
    
    # Development用Cookie設定（HTTP対応）
    SESSION_COOKIE_SECURE = False  # HTTP接続でもCookie有効
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Production用により強固な設定
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
