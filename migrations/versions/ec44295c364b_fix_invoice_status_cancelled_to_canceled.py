"""fix_invoice_status_cancelled_to_canceled

Revision ID: ec44295c364b
Revises: 20251104085416
Create Date: 2025-11-07 06:39:10.988612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec44295c364b'
down_revision = '20251104085416'
branch_labels = None
depends_on = None


def upgrade():
    # invoices テーブルの status カラムを 'cancelled' から 'canceled' に更新
    op.execute("UPDATE invoices SET status = 'canceled' WHERE status = 'cancelled'")
    
    # invoice_status_history テーブルの old_status カラムを 'cancelled' から 'canceled' に更新
    op.execute("UPDATE invoice_status_history SET old_status = 'canceled' WHERE old_status = 'cancelled'")
    
    # invoice_status_history テーブルの new_status カラムを 'cancelled' から 'canceled' に更新
    op.execute("UPDATE invoice_status_history SET new_status = 'canceled' WHERE new_status = 'cancelled'")


def downgrade():
    # ロールバック: 'canceled' を 'cancelled' に戻す
    op.execute("UPDATE invoices SET status = 'cancelled' WHERE status = 'canceled'")
    op.execute("UPDATE invoice_status_history SET old_status = 'cancelled' WHERE old_status = 'canceled'")
    op.execute("UPDATE invoice_status_history SET new_status = 'cancelled' WHERE new_status = 'canceled'")
