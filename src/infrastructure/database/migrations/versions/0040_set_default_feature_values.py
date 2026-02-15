"""set_default_feature_values

Revision ID: 0040
Revises: 0039
Create Date: 2026-01-17

"""
from alembic import op
import sqlalchemy as sa


revision = "0040"
down_revision = "0039"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Обновляем существующие записи в таблице settings
    # Устанавливаем значения по умолчанию для новых полей
    op.execute("""
        UPDATE settings
        SET features = jsonb_set(
            jsonb_set(
                jsonb_set(
                    jsonb_set(
                        features::jsonb,
                        '{balance_enabled}',
                        'false'::jsonb,
                        true
                    ),
                    '{promocodes_enabled}',
                    'false'::jsonb,
                    true
                ),
                '{extra_devices,enabled}',
                'false'::jsonb,
                true
            ),
            '{transfers,enabled}',
            'false'::jsonb,
            true
        )
        WHERE features IS NOT NULL
    """)


def downgrade() -> None:
    # Возвращаем старые значения
    op.execute("""
        UPDATE settings
        SET features = jsonb_set(
            jsonb_set(
                jsonb_set(
                    jsonb_set(
                        features::jsonb,
                        '{balance_enabled}',
                        'true'::jsonb,
                        true
                    ),
                    '{promocodes_enabled}',
                    'true'::jsonb,
                    true
                ),
                '{extra_devices,enabled}',
                'true'::jsonb,
                true
            ),
            '{transfers,enabled}',
            'true'::jsonb,
            true
        )
        WHERE features IS NOT NULL
    """)
