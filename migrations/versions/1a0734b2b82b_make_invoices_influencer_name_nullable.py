"""Make invoices.influencer_name nullable

Revision ID: 1a0734b2b82b
Revises: 8040182793ab
Create Date: 2025-10-09 09:17:35.576143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a0734b2b82b'
down_revision = '8040182793ab'
branch_labels = None
depends_on = None


def upgrade():
    """influencer_nameカラムのNOT NULL制約を削除"""
    op.alter_column('invoices', 'influencer_name',
                    existing_type=sa.String(length=100),
                    nullable=True)


def downgrade():
    pass
