"""Add index to projects (user_id, is_todo) for query optimization

Revision ID: 20251104085416
Revises: 251101092000
Create Date: 2025-11-04 08:54:16.000000

第3段階: インデックス追加
todos表示の遅延改善 - user_idとis_todoの複合インデックス追加
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251104085416'
down_revision = '251031101032'
branch_labels = None
depends_on = None


def upgrade():
    """
    projectsテーブルの(user_id, is_todo)に複合インデックスを追加
    最適化目的: todos一覧取得時のクエリ速度向上
    
    第3段階: インデックス追加
    todos表示の遅延改善
    """
    # PostgreSQLとSQLiteの両方に対応
    bind = op.get_bind()
    is_postgresql = bind.dialect.name == 'postgresql'
    
    # インデックス名
    index_name = 'idx_projects_user_todo'
    
    # インデックスが既に存在するかチェック
    from sqlalchemy import inspect
    inspector = inspect(bind)
    existing_indexes = [idx['name'] for idx in inspector.get_indexes('projects')]
    
    if index_name not in existing_indexes:
        if is_postgresql:
            # PostgreSQL用
            op.create_index(
                index_name,
                'projects',
                ['user_id', 'is_todo'],
                unique=False
            )
        else:
            # SQLite用
            op.create_index(
                index_name,
                'projects',
                ['user_id', 'is_todo'],
                unique=False
            )
        print(f"✅ インデックス作成完了: {index_name}")
    else:
        print(f"ℹ️  インデックスは既に存在します: {index_name}")


def downgrade():
    """
    projectsテーブルの(user_id, is_todo)複合インデックスを削除
    """
    index_name = 'idx_projects_user_todo'
    
    try:
        op.drop_index(index_name, table_name='projects')
        print(f"✅ インデックス削除完了: {index_name}")
    except Exception as e:
        print(f"⚠️  インデックス削除時にエラー: {e}")

