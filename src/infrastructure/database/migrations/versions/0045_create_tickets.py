"""Create tickets and ticket_messages tables.

Revision ID: 0045
Revises: 0044
Create Date: 2026-02-22

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0045"
down_revision: Union[str, None] = "0044"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create ticket tables."""
    # Enum type
    ticket_status = sa.Enum("OPEN", "ANSWERED", "CLOSED", name="ticket_status")
    ticket_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_telegram_id", sa.BigInteger, nullable=False, index=True),
        sa.Column("subject", sa.String(200), nullable=False),
        sa.Column("status", ticket_status, nullable=False, server_default="OPEN"),
        sa.Column("is_read_by_user", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("is_read_by_admin", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.timezone("UTC", sa.func.now()), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.timezone("UTC", sa.func.now()), nullable=False),
    )

    op.create_table(
        "ticket_messages",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ticket_id", sa.Integer, sa.ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("sender_telegram_id", sa.BigInteger, nullable=False),
        sa.Column("is_admin", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.timezone("UTC", sa.func.now()), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.timezone("UTC", sa.func.now()), nullable=False),
    )


def downgrade() -> None:
    """Drop ticket tables."""
    op.drop_table("ticket_messages")
    op.drop_table("tickets")

    ticket_status = sa.Enum("OPEN", "ANSWERED", "CLOSED", name="ticket_status")
    ticket_status.drop(op.get_bind(), checkfirst=True)
