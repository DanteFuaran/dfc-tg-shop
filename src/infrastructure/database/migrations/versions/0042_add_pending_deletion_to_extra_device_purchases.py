"""Add pending_deletion column to extra_device_purchases table.

Revision ID: 0042
Revises: 0041
Create Date: 2026-01-31

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0042"
down_revision: Union[str, None] = "0041"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add pending_deletion column to extra_device_purchases table."""
    conn = op.get_bind()
    conn.execute(sa.text("""
        ALTER TABLE extra_device_purchases 
        ADD COLUMN IF NOT EXISTS pending_deletion BOOLEAN NOT NULL DEFAULT FALSE
    """))


def downgrade() -> None:
    """Remove pending_deletion column from extra_device_purchases table."""
    conn = op.get_bind()
    conn.execute(sa.text("""
        ALTER TABLE extra_device_purchases 
        DROP COLUMN IF EXISTS pending_deletion
    """))
