"""Admin ticket management routes."""

from __future__ import annotations

from typing import Any

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from src.infrastructure.database import UnitOfWork
from src.services.ticket import TicketService
from src.web.dependencies import require_admin
from src.web.routers.tickets import ticket_to_dict

router = APIRouter(prefix="/api/admin/tickets", tags=["admin-tickets"])


@router.get("")
async def api_admin_get_tickets(request: Request, uid: int = Depends(require_admin)):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        tickets = await ticket_svc.get_all_tickets(uow)
        return JSONResponse([ticket_to_dict(t) for t in tickets])


@router.get("/{ticket_id}")
async def api_admin_get_ticket(ticket_id: int, request: Request, uid: int = Depends(require_admin)):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        ticket = await ticket_svc.get_ticket(uow, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        await ticket_svc.mark_read_by_admin(uow, ticket_id)
        return JSONResponse(ticket_to_dict(ticket))


@router.post("/{ticket_id}/reply")
async def api_admin_reply_ticket(ticket_id: int, request: Request, uid: int = Depends(require_admin)):
    body = await request.json()
    text = (body.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Введите сообщение")

    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        updated = await ticket_svc.add_reply(uow, ticket_id, uid, text, is_admin=True)
        if not updated:
            raise HTTPException(status_code=404, detail="Тикет не найден")

        return JSONResponse(ticket_to_dict(updated))


@router.post("/{ticket_id}/close")
async def api_admin_close_ticket(ticket_id: int, request: Request, uid: int = Depends(require_admin)):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        closed = await ticket_svc.close_ticket(uow, ticket_id)
        if not closed:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        return JSONResponse(ticket_to_dict(closed))


@router.delete("/{ticket_id}")
async def api_admin_delete_ticket(ticket_id: int, request: Request, uid: int = Depends(require_admin)):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        deleted = await ticket_svc.delete_ticket(uow, ticket_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Тикет не найден")
        return JSONResponse({"ok": True})


@router.patch("/{ticket_id}/messages/{msg_id}")
async def api_admin_edit_ticket_message(
    ticket_id: int, msg_id: int, request: Request, uid: int = Depends(require_admin),
):
    """Admin: edit own (admin) message in any ticket."""
    body = await request.json()
    text = (body.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Текст не может быть пустым")
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        ticket_svc: TicketService = await req_container.get(TicketService)
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        msg = await ticket_svc.edit_message(uow, msg_id, text, uid, is_admin=True)
        if not msg:
            raise HTTPException(status_code=403, detail="Нет доступа")
        return JSONResponse({"ok": True, "id": msg.id, "text": msg.text})


@router.delete("/{ticket_id}/messages/{msg_id}")
async def api_admin_delete_ticket_message(
    ticket_id: int, msg_id: int, request: Request, uid: int = Depends(require_admin),
):
    """Admin: delete any message in any ticket."""
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        uow: UnitOfWork = await req_container.get(UnitOfWork)
        # Admin can delete any message
        msg = await uow.repository.tickets.get_message_by_id(msg_id)
        if not msg:
            raise HTTPException(status_code=404, detail="Сообщение не найдено")
        await uow.repository.tickets.delete_message_by_id(msg_id)
        await uow.commit()
        return JSONResponse({"ok": True})
