"""Add linked_project_id and linked_invoice_id to projects for BerryWork/BerryPay integration

Revision ID: 20251001132853
Revises: 88202d3a053d
Create Date: 2025-10-01 13:28:53

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251001132853'
down_revision = '88202d3a053d'
branch_labels = None
depends_on = None


def upgrade():
    # Add linked_project_id column
    op.add_column('projects', sa.Column('linked_project_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_projects_linked_project_id', 'projects', 'projects', ['linked_project_id'], ['id'])
    
    # Add linked_invoice_id column
    op.add_column('projects', sa.Column('linked_invoice_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_projects_linked_invoice_id', 'projects', 'invoices', ['linked_invoice_id'], ['id'])


def downgrade():
    # Remove foreign keys
    op.drop_constraint('fk_projects_linked_invoice_id', 'projects', type_='foreignkey')
    op.drop_constraint('fk_projects_linked_project_id', 'projects', type_='foreignkey')
    
    # Remove columns
    op.drop_column('projects', 'linked_invoice_id')
    op.drop_column('projects', 'linked_project_id')