"""add_promocodes_enabled_to_features

Revision ID: 0039
Revises: 0038
Create Date: 2026-01-17

"""
from alembic import op
import sqlalchemy as sa


revision = "0039"
down_revision = "0038"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Обновляем существующие записи в таблице settings
    # Добавляем promocodes_enabled = true в features JSON
    op.execute("""
        UPDATE settings
        SET features = jsonb_set(
            features::jsonb,
            '{promocodes_enabled}',
            'true'::jsonb,
            true
        )
        WHERE features IS NOT NULL
    """)


def downgrade() -> None:
    # Удаляем promocodes_enabled из features JSON
    op.execute("""
        UPDATE settings
        SET features = features::jsonb - 'promocodes_enabled'
        WHERE features IS NOT NULL
    """)
