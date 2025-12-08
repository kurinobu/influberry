"""Add TikTok OAuth fields

Revision ID: 20251207120000
Revises: ec44295c364b
Create Date: 2025-12-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251207120000'
down_revision = 'ec44295c364b'
branch_labels = None
depends_on = None


def upgrade():
    # TikTok OAuth用フィールド追加
    op.add_column('users', sa.Column('tiktok_id', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('tiktok_username', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('tiktok_avatar_url', sa.String(500), nullable=True))
    op.add_column('users', sa.Column('oauth_provider', sa.String(20), nullable=True))
    
    # インデックス追加（tiktok_idでの検索最適化）
    op.create_index('idx_users_tiktok_id', 'users', ['tiktok_id'], unique=False)
    
    # 既存ユーザーのoauth_providerをデフォルト値'email'に設定
    op.execute("UPDATE users SET oauth_provider = 'email' WHERE oauth_provider IS NULL")


def downgrade():
    # インデックス削除
    op.drop_index('idx_users_tiktok_id', table_name='users')
    
    # カラム削除
    op.drop_column('users', 'oauth_provider')
    op.drop_column('users', 'tiktok_avatar_url')
    op.drop_column('users', 'tiktok_username')
    op.drop_column('users', 'tiktok_id')