"""Add bot_locale column to settings table.

Revision ID: 0041
Revises: 0040
Create Date: 2026-01-24

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0041"
down_revision: Union[str, None] = "0040"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add bot_locale column to settings table using raw SQL
    # The 'locale' enum type already exists (used in users table)
    # Using UPPERCASE value as defined in migration 0001
    conn = op.get_bind()
    conn.execute(sa.text("""
        ALTER TABLE settings 
        ADD COLUMN IF NOT EXISTS bot_locale locale NOT NULL DEFAULT 'RU'
    """))


def downgrade() -> None:
    op.drop_column('settings', 'bot_locale')
