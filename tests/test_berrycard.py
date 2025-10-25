"""
BerryCard機能のテスト
"""
import pytest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.models.user import User

@pytest.fixture
def app():
    """テスト用アプリケーション"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

@pytest.fixture
def client(app):
    """テストクライアント"""
    return app.test_client()

@pytest.fixture
def db(app):
    """テストデータベース"""
    with app.app_context():
        from app import db
        db.create_all()
        yield db
        db.drop_all()

def test_berrycard_profile_creation(db):
    """BerryCardプロフィール作成テスト"""
    user = User(
        username="testuser",
        email="test@example.com",
        password="test_password",
        influencer_name="テストユーザー",
        bio="テスト自己紹介",
        profile_public=True
    )
    db.session.add(user)
    db.session.commit()
    
    assert user.id is not None
    assert user.influencer_name == "テストユーザー"
    assert user.bio == "テスト自己紹介"
    assert user.profile_public is True

def test_berrycard_profile_update(db):
    """BerryCardプロフィール更新テスト"""
    user = User(
        username="testuser",
        email="test@example.com",
        password="test_password",
        influencer_name="テストユーザー",
        bio="テスト自己紹介",
        profile_public=False
    )
    db.session.add(user)
    db.session.commit()
    
    # プロフィール更新
    user.influencer_name = "更新されたユーザー"
    user.bio = "更新された自己紹介"
    user.profile_public = True
    db.session.commit()
    
    assert user.influencer_name == "更新されたユーザー"
    assert user.bio == "更新された自己紹介"
    assert user.profile_public is True

def test_berrycard_profile_validation(db):
    """BerryCardプロフィールバリデーションテスト"""
    # 必須フィールドのテスト
    user = User(
        username="testuser",
        email="test@example.com",
        password="test_password",
        influencer_name="",  # 空文字
        bio="テスト自己紹介"
    )
    
    # バリデーションエラーが発生することを確認
    with pytest.raises(Exception):
        db.session.add(user)
        db.session.commit()

def test_berrycard_profile_social_links(db):
    """BerryCardソーシャルリンクテスト"""
    user = User(
        username="testuser",
        email="test@example.com",
        password="test_password",
        influencer_name="テストユーザー",
        bio="テスト自己紹介",
        website_url="https://example.com",
        instagram_url="https://instagram.com/test",
        twitter_url="https://twitter.com/test",
        youtube_url="https://youtube.com/test",
        tiktok_url="https://tiktok.com/test"
    )
    db.session.add(user)
    db.session.commit()
    
    assert user.website_url == "https://example.com"
    assert user.instagram_url == "https://instagram.com/test"
    assert user.twitter_url == "https://twitter.com/test"
    assert user.youtube_url == "https://youtube.com/test"
    assert user.tiktok_url == "https://tiktok.com/test"

def test_berrycard_profile_design_settings(db):
    """BerryCardデザイン設定テスト"""
    user = User(
        username="testuser",
        email="test@example.com",
        password="test_password",
        influencer_name="テストユーザー",
        bio="テスト自己紹介",
        card_color="peach",
        card_font="Nunito",
        card_layout="simple"
    )
    db.session.add(user)
    db.session.commit()
    
    assert user.card_color == "peach"
    assert user.card_font == "Nunito"
    assert user.card_layout == "simple"

def test_berrycard_profile_completion_percentage(db):
    """BerryCardプロフィール完成度テスト"""
    # 基本情報のみ
    user1 = User(
        username="testuser1",
        email="test1@example.com",
        password="test_password",
        influencer_name="テストユーザー1",
        bio="テスト自己紹介1"
    )
    
    # ソーシャルリンク追加
    user2 = User(
        username="testuser2",
        email="test2@example.com",
        password="test_password",
        influencer_name="テストユーザー2",
        bio="テスト自己紹介2",
        website_url="https://example.com",
        instagram_url="https://instagram.com/test"
    )
    
    # プロフィール画像追加
    user3 = User(
        username="testuser3",
        email="test3@example.com",
        password="test_password",
        influencer_name="テストユーザー3",
        bio="テスト自己紹介3",
        website_url="https://example.com",
        instagram_url="https://instagram.com/test",
        icon_filename="icon.jpg"
    )
    
    db.session.add_all([user1, user2, user3])
    db.session.commit()
    
    # 完成度の計算（簡易版）
    def calculate_completion(user):
        score = 0
        if user.influencer_name:
            score += 20
        if user.bio:
            score += 20
        if user.website_url or user.instagram_url or user.twitter_url or user.youtube_url or user.tiktok_url:
            score += 20
        if user.icon_filename:
            score += 20
        if user.profile_public:
            score += 20
        return score
    
    assert calculate_completion(user1) == 60  # 名前、自己紹介、公開状態
    assert calculate_completion(user2) == 80  # 名前、自己紹介、ソーシャルリンク、公開状態
    assert calculate_completion(user3) == 100  # 全て設定済み

if __name__ == "__main__":
    pytest.main([__file__])
