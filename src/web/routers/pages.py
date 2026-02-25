"""HTML page routes — serves React Mini App as SPA."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.core.config import AppConfig
from src.web.dependencies import get_current_user_id

WEB_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = WEB_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


def _miniapp_index(request: Request) -> FileResponse:
    """Return React miniapp index.html (built by Vite)."""
    dist: Path = request.app.state.miniapp_dist
    return FileResponse(str(dist / "index.html"), media_type="text/html")


@router.get("/", response_class=HTMLResponse)
async def web_index(request: Request, access_token: Optional[str] = Cookie(default=None)):
    """Landing — redirect to dashboard if authenticated, else to login."""
    uid = await get_current_user_id(request, access_token)
    if uid:
        return RedirectResponse(url="/web/dashboard", status_code=302)
    return RedirectResponse(url="/web/login", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def web_login_page(request: Request):
    config: AppConfig = request.app.state.config
    domain = config.domain.get_secret_value()
    return templates.TemplateResponse("login.html", {"request": request, "domain": domain})


@router.get("/dashboard", response_class=HTMLResponse)
async def web_dashboard_page(request: Request, access_token: Optional[str] = Cookie(default=None)):
    uid = await get_current_user_id(request, access_token)
    if not uid:
        return RedirectResponse(url="/web/login", status_code=302)
    return _miniapp_index(request)


@router.get("/miniapp", response_class=HTMLResponse)
async def miniapp_page(request: Request):
    """Telegram Mini App entry point — auth via initData."""
    return _miniapp_index(request)


@router.get("/miniapp/{path:path}", response_class=HTMLResponse)
async def miniapp_spa_fallback(request: Request, path: str = ""):
    """SPA catch-all — serve React index.html for all client-side routes."""
    return _miniapp_index(request)
