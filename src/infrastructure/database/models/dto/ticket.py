"""Ticket DTOs."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from src.core.enums import TicketStatus

from .base import BaseDto


class TicketMessageDto(BaseDto):
    id: int
    ticket_id: int
    sender_telegram_id: int
    is_admin: bool = False
    text: str
    created_at: datetime


class TicketDto(BaseDto):
    id: int
    user_telegram_id: int
    subject: str
    status: TicketStatus = TicketStatus.OPEN
    is_read_by_user: bool = True
    is_read_by_admin: bool = False
    messages: list[TicketMessageDto] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
