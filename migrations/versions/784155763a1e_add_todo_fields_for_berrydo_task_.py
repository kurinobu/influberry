"""Add todo fields for BerryDo task management integration

Revision ID: 784155763a1e
Revises: f12568e353c7
Create Date: 2025-09-20 06:26:09.533849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '784155763a1e'
down_revision = 'f12568e353c7'
branch_labels = None
depends_on = None


def upgrade():
    # Todo機能用拡張フィールド追加
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('todo_priority', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('todo_importance', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('todo_status', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('is_todo', sa.Boolean(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('todo_title', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('todo_description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('todo_due_date', sa.Date(), nullable=True))

def downgrade():
    # Todo機能用フィールド削除
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('todo_due_date')
        batch_op.drop_column('todo_description')
        batch_op.drop_column('todo_title')
        batch_op.drop_column('is_todo')
        batch_op.drop_column('todo_status')
        batch_op.drop_column('todo_importance')
        batch_op.drop_column('todo_priority')
