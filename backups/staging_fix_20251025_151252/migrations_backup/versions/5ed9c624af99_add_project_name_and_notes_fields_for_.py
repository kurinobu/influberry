"""Add project_name and notes fields for extensible architecture

Revision ID: 5ed9c624af99
Revises: fb6bc9aa7119
Create Date: 2025-09-11 11:03:27.934879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ed9c624af99'
down_revision = 'fb6bc9aa7119'
branch_labels = None
depends_on = None


def upgrade():
    # 段階的カラム追加（nullable=True で安全実装）
    op.add_column('projects', sa.Column('project_name', sa.String(255), nullable=True))
    op.add_column('projects', sa.Column('notes', sa.Text, nullable=True))
    
    # 既存データ自動補完（データ損失防止）
    op.execute("UPDATE projects SET project_name = company_name WHERE project_name IS NULL")

def downgrade():
    op.drop_column('projects', 'notes')
    op.drop_column('projects', 'project_name')
