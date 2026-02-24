"""User ticket routes (support system)."""

from __future__ import annotations

from typing import Any

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger

from src.core.enums import UserRole
from src.infrastructure.database import UnitOfWork
from src.services.ticket import TicketService
from src.services.user import UserService
from src.web.dependencies import require_auth


router = APIRouter(prefix="/api/tickets", tags=["tickets"])


# ── Shared helper ─────────────────────────────────────────────────


def ticket_to_dict(t: Any) -> dict[str, Any]:
    """Convert TicketDto to JSON-serialisable dict."""
    return {
        "id": t.id,
        "subject": t.subject,
        "status": t.status.value if hasattr(t.status, "value") else str(t.status),
        "user_telegram_id": t.user_telegram_id,
        "is_read_by_user": t.is_read_by_user,
        "is_read_by_admin": t.is_read_by_admin,
        "created_at": t.created_at.strftime("%d.%m.%Y %H:%M") if t.created_at else "",
        "updated_at": t.updated_at.strftime("%d.%m.%Y %H:%M") if t.updated_at else "",
        "messages": [
            {
                "id": m.id,
                "is_admin": m.is_admin,
                "text": m.text,
                "created_at": m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else "",
            }
            for m in (t.messages or [])
        ],
    }


# ══════════════════════════════════════════════════════════════════
# USER TICKETS
# ══════════════════════════════════════════════════════════════════


@router.get("")
async def api_get_tickets(request: Request, uid: int = Depends(require_auth)):
    """User: get own tickets."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        tickets = await ticket_svc.get_user_tickets(uow, uid)
        return JSONResponse([ticket_to_dict(t) for t in tickets])


@router.post("")
async def api_create_ticket(request: Request, uid: int = Depends(require_auth)):
    """User: create a new ticket."""
    body = await request.json()
    subject = (body.get("subject") or "").strip()
    text = (body.get("text") or "").strip()
    if not subject or not text:
        raise HTTPException(status_code=400, detail="Заполните тему и сообщение")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.create_ticket(uow, uid, subject, text)

        # Notify admins/devs via bot (with close button, no auto-delete)
        try:
            from src.services.notification import NotificationService
            from src.core.utils.message_payload import MessagePayload

            ntf: NotificationService = await req_container.get(NotificationService)
            user_service: UserService = await req_container.get(UserService)
            user = await user_service.get(telegram_id=uid)
            user_label = f"{user.name} (@{user.username})" if user and user.username else (user.name if user else str(uid))
            ticket_text = f"🎫 Новый тикет #{ticket.id}\n\n👤 {user_label}\n📝 {subject}\n\n{text[:300]}"
            payload = MessagePayload.not_deleted(text=ticket_text)
            # Send to all DEV and ADMIN users
            devs = await user_service.get_by_role(role=UserRole.DEV)
            admins = await user_service.get_by_role(role=UserRole.ADMIN)
            recipients = {u.telegram_id: u for u in (devs or []) + (admins or [])}
            for recipient in recipients.values():
                try:
                    await ntf.notify_user(user=recipient, payload=payload)
                except Exception:
                    pass
        except Exception:
            pass

        return JSONResponse(ticket_to_dict(ticket))


@router.get("/{ticket_id}")
async def api_get_ticket(ticket_id: int, request: Request, uid: int = Depends(require_auth)):
    """User: get ticket detail. Mark as read."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket or ticket.user_telegram_id != uid:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        await ticket_svc.mark_read_by_user(uow, ticket_id)
        return JSONResponse(ticket_to_dict(ticket))


@router.post("/{ticket_id}/reply")
async def api_reply_ticket(ticket_id: int, request: Request, uid: int = Depends(require_auth)):
    """User: reply to own ticket."""
    body = await request.json()
    text = (body.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Введите сообщение")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        # Verify ownership
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket or ticket.user_telegram_id != uid:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        if ticket.status == "CLOSED":
            raise HTTPException(status_code=400, detail="Тикет закрыт")

        updated = await ticket_svc.add_reply(uow, ticket_id, uid, text, is_admin=False)
        return JSONResponse(ticket_to_dict(updated))


@router.post("/{ticket_id}/close")
async def api_close_ticket(ticket_id: int, request: Request, uid: int = Depends(require_auth)):
    """User: close own ticket."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket or ticket.user_telegram_id != uid:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        closed = await ticket_svc.close_ticket(uow, ticket_id)
        return JSONResponse(ticket_to_dict(closed))


@router.patch("/{ticket_id}/messages/{msg_id}")
async def api_edit_ticket_message(
    ticket_id: int, msg_id: int, request: Request, uid: int = Depends(require_auth),
):
    """User: edit own message in own ticket."""
    body = await request.json()
    text = (body.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Текст не может быть пустым")
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket or ticket.user_telegram_id != uid:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        msg = await ticket_svc.edit_message(uow, msg_id, text, uid, is_admin=False)
        if not msg:
            raise HTTPException(status_code=403, detail="Нет доступа")
        return JSONResponse({"ok": True, "id": msg.id, "text": msg.text})


@router.delete("/{ticket_id}/messages/{msg_id}")
async def api_delete_ticket_message(
    ticket_id: int, msg_id: int, request: Request, uid: int = Depends(require_auth),
):
    """User: delete own message in own ticket."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket or ticket.user_telegram_id != uid:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        ok = await ticket_svc.delete_message(uow, msg_id, uid, is_admin=False)
        if not ok:
            raise HTTPException(status_code=403, detail="Нет доступа")
        return JSONResponse({"ok": True})
