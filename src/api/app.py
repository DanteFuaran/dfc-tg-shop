from aiogram import Dispatcher
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from src.api.endpoints import TelegramWebhookEndpoint, connect_router, payments_router, remnawave_router
from src.core.config import AppConfig
from src.lifespan import lifespan
from src.services.mirror_bot_manager import MirrorBotManager
from src.web.router import WEB_DIR
from src.web.router import router as web_router

# React miniapp build directory (copied from frontend-builder in Docker)
import pathlib as _pl
_MINIAPP_DIST = _pl.Path("/opt/dfc-tg/miniapp-dist")


def create_app(config: AppConfig, dispatcher: Dispatcher) -> FastAPI:
    app: FastAPI = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(connect_router)
    app.include_router(payments_router)
    app.include_router(remnawave_router)

    # Web cabinet + Mini App
    app.mount("/web/static", StaticFiles(directory=str(WEB_DIR / "static")), name="web-static")

    # React miniapp assets (JS/CSS bundles)
    # Mounted at both paths: Vite may output /assets/ or /web/miniapp/assets/
    if _MINIAPP_DIST.exists():
        app.mount(
            "/web/miniapp/assets",
            StaticFiles(directory=str(_MINIAPP_DIST / "assets")),
            name="miniapp-assets",
        )
        # Also serve at /assets/ — Vite default base '/' produces these paths
        app.mount(
            "/assets",
            StaticFiles(directory=str(_MINIAPP_DIST / "assets")),
            name="miniapp-assets-root",
        )

    app.include_router(web_router, prefix="/web")
    app.state.config = config
    app.state.miniapp_dist = _MINIAPP_DIST

    # Root redirect — so bare domain goes to web cabinet
    @app.get("/", include_in_schema=False)
    async def root_redirect():
        return RedirectResponse(url="/web/", status_code=302)

    telegram_webhook_endpoint = TelegramWebhookEndpoint(
        dispatcher=dispatcher,
        secret_token=config.bot.secret_token.get_secret_value(),
    )
    telegram_webhook_endpoint.register(app=app, path=config.bot.webhook_path)
    app.state.telegram_webhook_endpoint = telegram_webhook_endpoint
    app.state.dispatcher = dispatcher

    # Mirror bot manager — handles additional bot webhooks
    mirror_bot_manager = MirrorBotManager(dispatcher=dispatcher, domain=config.domain)
    mirror_bot_manager.register_routes(app)
    app.state.mirror_bot_manager = mirror_bot_manager
    dispatcher["mirror_bot_manager"] = mirror_bot_manager

    return app
