"""HTML page routes — serves React Mini App as SPA for all routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

router = APIRouter()


def _miniapp_index(request: Request) -> FileResponse:
    """Return React miniapp index.html (built by Vite)."""
    dist: Path = request.app.state.miniapp_dist
    return FileResponse(str(dist / "index.html"), media_type="text/html")


@router.get("/", response_class=HTMLResponse)
async def web_index(request: Request):
    return RedirectResponse(url="/web/miniapp", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def web_login_page(request: Request):
    """Old login route — redirect to miniapp (auth is handled automatically via Telegram initData)."""
    return RedirectResponse(url="/web/miniapp", status_code=302)


@router.get("/dashboard", response_class=HTMLResponse)
async def web_dashboard_page(request: Request):
    return _miniapp_index(request)


@router.get("/miniapp", response_class=HTMLResponse)
async def miniapp_page(request: Request):
    return _miniapp_index(request)


@router.get("/miniapp/{path:path}", response_class=HTMLResponse)
async def miniapp_spa_fallback(request: Request, path: str = ""):
    return _miniapp_index(request)
