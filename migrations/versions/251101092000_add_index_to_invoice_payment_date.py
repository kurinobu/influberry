"""Add index to invoice payment_date for query optimization

Revision ID: 251101092000
Revises: 251031101032
Create Date: 2025-11-01 09:20:00.000000

Phase 1 Query Optimization: 修正案3
優先度1: データベースクエリの最適化（緊急）
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '251101092000'
down_revision = '251031101032'
branch_labels = None
depends_on = None


def upgrade():
    """
    Invoice.payment_dateにインデックスを追加
    最適化目的: 支払済み請求書の集計時のクエリ速度向上
    
    優先度1: データベースクエリの最適化（緊急）
    修正案3: Invoice.payment_dateへのインデックス追加
    """
    # PostgreSQLとSQLiteの両方に対応
    bind = op.get_bind()
    is_postgresql = bind.dialect.name == 'postgresql'
    
    # インデックス名
    index_name = 'ix_invoice_payment_date'
    
    # インデックスが既に存在するかチェック
    from sqlalchemy import inspect
    inspector = inspect(bind)
    existing_indexes = [idx['name'] for idx in inspector.get_indexes('invoices')]
    
    if index_name not in existing_indexes:
        if is_postgresql:
            # PostgreSQL用
            op.create_index(
                index_name,
                'invoices',
                ['payment_date'],
                unique=False
            )
        else:
            # SQLite用
            op.create_index(
                index_name,
                'invoices',
                ['payment_date'],
                unique=False
            )
        print(f"✅ インデックス作成完了: {index_name}")
    else:
        print(f"ℹ️  インデックスは既に存在します: {index_name}")


def downgrade():
    """
    Invoice.payment_dateのインデックスを削除
    """
    index_name = 'ix_invoice_payment_date'
    
    try:
        op.drop_index(index_name, table_name='invoices')
        print(f"✅ インデックス削除完了: {index_name}")
    except Exception as e:
        print(f"⚠️  インデックス削除時にエラー: {e}")

