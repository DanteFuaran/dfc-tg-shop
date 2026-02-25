"""Admin monitoring routes — Remnawave system stats."""

from __future__ import annotations

from dishka import AsyncContainer, Scope
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from src.services.remnawave import RemnawaveService
from src.web.dependencies import require_admin

router = APIRouter(prefix="/api/admin/monitoring", tags=["admin-monitoring"])


@router.get("")
async def api_admin_monitoring(request: Request, uid: int = Depends(require_admin)):
    container: AsyncContainer = request.app.state.dishka_container
    async with container(scope=Scope.REQUEST) as req_container:
        remna_svc: RemnawaveService = await req_container.get(RemnawaveService)
        try:
            stats = await remna_svc.remnawave.system.get_stats()
            if stats is None:
                return JSONResponse({"error": "Нет данных от панели"}, status_code=503)

            # Serialize to dict — remnapy models inherit from pydantic BaseModel
            data = stats.model_dump() if hasattr(stats, "model_dump") else vars(stats)
            return JSONResponse(data)
        except Exception as e:
            return JSONResponse(
                {"error": f"Ошибка соединения с Remnawave: {e}"},
                status_code=503,
            )
