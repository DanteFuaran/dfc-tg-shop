"""Ticket repository."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import desc

from src.infrastructure.database.models.sql.ticket import Ticket, TicketMessage

from .base import BaseRepository


class TicketRepository(BaseRepository):
    async def create(self, ticket: Ticket) -> Ticket:
        return await self.create_instance(ticket)

    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return await self._get_one(Ticket, Ticket.id == ticket_id)

    async def get_by_user(self, telegram_id: int) -> list[Ticket]:
        return await self._get_many(
            Ticket,
            Ticket.user_telegram_id == telegram_id,
            order_by=desc(Ticket.updated_at),
        )

    async def get_all(self) -> list[Ticket]:
        return await self._get_many(Ticket, order_by=desc(Ticket.updated_at))

    async def update(self, ticket_id: int, **kwargs) -> Optional[Ticket]:
        return await self._update(Ticket, Ticket.id == ticket_id, **kwargs)

    async def delete(self, ticket_id: int) -> int:
        return await self._delete(Ticket, Ticket.id == ticket_id)

    async def add_message(self, message: TicketMessage) -> TicketMessage:
        return await self.create_instance(message)

    async def get_message_by_id(self, msg_id: int) -> Optional[TicketMessage]:
        return await self._get_one(TicketMessage, TicketMessage.id == msg_id)

    async def update_message(self, msg_id: int, **kwargs) -> Optional[TicketMessage]:
        return await self._update(TicketMessage, TicketMessage.id == msg_id, **kwargs)

    async def delete_message_by_id(self, msg_id: int) -> int:
        return await self._delete(TicketMessage, TicketMessage.id == msg_id)

    async def count_unread_for_user(self, telegram_id: int) -> int:
        return await self._count(
            Ticket,
            Ticket.user_telegram_id == telegram_id,
            Ticket.is_read_by_user == False,
        )

    async def count_unread_for_admin(self) -> int:
        return await self._count(Ticket, Ticket.is_read_by_admin == False)
