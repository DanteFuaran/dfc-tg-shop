from typing import Sequence, Union

from alembic import op

revision: str = "0046"
down_revision: Union[str, None] = "0045"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add LAVA and PLATEGA to payment_gateway_type enum
    op.execute("ALTER TYPE payment_gateway_type ADD VALUE IF NOT EXISTS 'LAVA'")
    op.execute("ALTER TYPE payment_gateway_type ADD VALUE IF NOT EXISTS 'PLATEGA'")


def downgrade() -> None:
    # PostgreSQL doesn't support removing enum values
    pass
