"""Support ticket models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums import TicketStatus

from .base import BaseSql
from .timestamp import TimestampMixin


class Ticket(BaseSql, TimestampMixin):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus, name="ticket_status", create_constraint=True, validate_strings=True),
        nullable=False,
        server_default="OPEN",
    )
    is_read_by_user: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    is_read_by_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    messages: Mapped[list["TicketMessage"]] = relationship(
        "TicketMessage",
        back_populates="ticket",
        order_by="TicketMessage.created_at.asc()",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class TicketMessage(BaseSql, TimestampMixin):
    __tablename__ = "ticket_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sender_telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    text: Mapped[str] = mapped_column(Text, nullable=False)

    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="messages")
