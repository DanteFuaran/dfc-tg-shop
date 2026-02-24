"""Ticket service — create, reply, close support tickets."""

from __future__ import annotations

from typing import Optional

from loguru import logger

from src.core.enums import TicketStatus
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto.ticket import TicketDto, TicketMessageDto
from src.infrastructure.database.models.sql.ticket import Ticket, TicketMessage


class TicketService:
    """Stateless service — requires UnitOfWork passed to every method."""

    # ── Create ────────────────────────────────────────────────────

    async def create_ticket(
        self,
        uow: UnitOfWork,
        user_telegram_id: int,
        subject: str,
        text: str,
    ) -> TicketDto:
        ticket = Ticket(
            user_telegram_id=user_telegram_id,
            subject=subject,
            status=TicketStatus.OPEN,
            is_read_by_user=True,
            is_read_by_admin=False,
        )
        ticket = await uow.repository.tickets.create(ticket)

        msg = TicketMessage(
            ticket_id=ticket.id,
            sender_telegram_id=user_telegram_id,
            is_admin=False,
            text=text,
        )
        await uow.repository.tickets.add_message(msg)

        # Reload with messages
        ticket = await uow.repository.tickets.get_by_id(ticket.id)
        logger.info(f"Ticket #{ticket.id} created by {user_telegram_id}")
        return TicketDto.from_model(ticket)

    # ── Reply ─────────────────────────────────────────────────────

    async def add_reply(
        self,
        uow: UnitOfWork,
        ticket_id: int,
        sender_telegram_id: int,
        text: str,
        is_admin: bool = False,
    ) -> Optional[TicketDto]:
        ticket = await uow.repository.tickets.get_by_id(ticket_id)
        if not ticket:
            return None

        msg = TicketMessage(
            ticket_id=ticket_id,
            sender_telegram_id=sender_telegram_id,
            is_admin=is_admin,
            text=text,
        )
        await uow.repository.tickets.add_message(msg)

        # Update status + read flags
        if is_admin:
            await uow.repository.tickets.update(
                ticket_id,
                status=TicketStatus.ANSWERED,
                is_read_by_user=False,
                is_read_by_admin=True,
            )
        else:
            await uow.repository.tickets.update(
                ticket_id,
                status=TicketStatus.OPEN,
                is_read_by_admin=False,
                is_read_by_user=True,
            )

        ticket = await uow.repository.tickets.get_by_id(ticket_id)
        return TicketDto.from_model(ticket)

    # ── Read ──────────────────────────────────────────────────────

    async def get_user_tickets(
        self, uow: UnitOfWork, telegram_id: int
    ) -> list[TicketDto]:
        tickets = await uow.repository.tickets.get_by_user(telegram_id)
        return TicketDto.from_model_list(tickets)

    async def get_all_tickets(self, uow: UnitOfWork) -> list[TicketDto]:
        tickets = await uow.repository.tickets.get_all()
        return TicketDto.from_model_list(tickets)

    async def get_ticket(self, uow: UnitOfWork, ticket_id: int) -> Optional[TicketDto]:
        ticket = await uow.repository.tickets.get_by_id(ticket_id)
        return TicketDto.from_model(ticket) if ticket else None

    # ── Mark read ────────────────────────────────────────────────

    async def mark_read_by_user(self, uow: UnitOfWork, ticket_id: int) -> None:
        await uow.repository.tickets.update(ticket_id, is_read_by_user=True)

    async def mark_read_by_admin(self, uow: UnitOfWork, ticket_id: int) -> None:
        await uow.repository.tickets.update(ticket_id, is_read_by_admin=True)

    # ── Message edit / delete ─────────────────────────────────────

    async def edit_message(
        self,
        uow: UnitOfWork,
        msg_id: int,
        new_text: str,
        sender_telegram_id: int,
        is_admin: bool = False,
    ) -> Optional[TicketMessageDto]:
        msg = await uow.repository.tickets.get_message_by_id(msg_id)
        if not msg:
            return None
        # Only own messages can be edited (admin can edit all admin messages)
        if not is_admin and msg.sender_telegram_id != sender_telegram_id:
            return None
        if is_admin and not msg.is_admin:
            return None
        updated = await uow.repository.tickets.update_message(msg_id, text=new_text)
        await uow.commit()
        return TicketMessageDto.from_model(updated) if updated else None

    async def delete_message(
        self,
        uow: UnitOfWork,
        msg_id: int,
        sender_telegram_id: int,
        is_admin: bool = False,
    ) -> bool:
        msg = await uow.repository.tickets.get_message_by_id(msg_id)
        if not msg:
            return False
        if not is_admin and msg.sender_telegram_id != sender_telegram_id:
            return False
        await uow.repository.tickets.delete_message_by_id(msg_id)
        await uow.commit()
        return True

    # ── Close / Delete ───────────────────────────────────────────

    async def close_ticket(self, uow: UnitOfWork, ticket_id: int) -> Optional[TicketDto]:
        ticket = await uow.repository.tickets.update(
            ticket_id, status=TicketStatus.CLOSED
        )
        return TicketDto.from_model(ticket) if ticket else None

    async def delete_ticket(self, uow: UnitOfWork, ticket_id: int) -> bool:
        return await uow.repository.tickets.delete(ticket_id) > 0

    # ── Counters ─────────────────────────────────────────────────

    async def count_unread_user(self, uow: UnitOfWork, telegram_id: int) -> int:
        return await uow.repository.tickets.count_unread_for_user(telegram_id)

    async def count_unread_admin(self, uow: UnitOfWork) -> int:
        return await uow.repository.tickets.count_unread_for_admin()
