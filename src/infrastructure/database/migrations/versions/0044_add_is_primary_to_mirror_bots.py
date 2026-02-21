"""Add is_primary column to mirror_bots table.

Revision ID: 0044
Revises: 0043
Create Date: 2026-02-21

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0044"
down_revision: Union[str, None] = "0043"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add is_primary column to mirror_bots."""
    conn = op.get_bind()
    conn.execute(sa.text("""
        ALTER TABLE mirror_bots
        ADD COLUMN IF NOT EXISTS is_primary BOOLEAN NOT NULL DEFAULT FALSE
    """))


def downgrade() -> None:
    """Remove is_primary column from mirror_bots."""
    conn = op.get_bind()
    conn.execute(sa.text("""
        ALTER TABLE mirror_bots DROP COLUMN IF EXISTS is_primary
    """))
