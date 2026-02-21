"""Create mirror_bots table.

Revision ID: 0043
Revises: 0042
Create Date: 2026-02-21

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0043"
down_revision: Union[str, None] = "0042"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create mirror_bots table."""
    conn = op.get_bind()
    conn.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS mirror_bots (
            id SERIAL PRIMARY KEY,
            token VARCHAR NOT NULL UNIQUE,
            username VARCHAR NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT (TIMEZONE('UTC', NOW())),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT (TIMEZONE('UTC', NOW()))
        )
    """))


def downgrade() -> None:
    """Drop mirror_bots table."""
    conn = op.get_bind()
    conn.execute(sa.text("DROP TABLE IF EXISTS mirror_bots"))
