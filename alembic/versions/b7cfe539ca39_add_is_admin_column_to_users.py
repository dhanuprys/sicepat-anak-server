"""add_is_admin_column_to_users

Revision ID: b7cfe539ca39
Revises: 83b62ab3582e
Create Date: 2025-09-13 18:04:49.356173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7cfe539ca39'
down_revision = '83b62ab3582e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_admin column to users table
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))


def downgrade() -> None:
    # Remove is_admin column from users table
    op.drop_column('users', 'is_admin')
