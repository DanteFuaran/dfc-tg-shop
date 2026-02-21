"""
Mirror Bot Manager — manages the lifecycle of mirror (additional) bots.

Each mirror bot receives its own webhook endpoint and processes updates
through the same dispatcher as the main bot. This allows multiple Telegram
bots to function identically (same menus, handlers, logic) but under
different bot usernames.
"""

import asyncio
import secrets
from typing import Any, Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import SetWebhook, TelegramMethod
from aiogram.types import Update
from fastapi import Body, FastAPI, Header, HTTPException, Response, status
from loguru import logger
from pydantic import SecretStr
from typing_extensions import Annotated

from src.bot.storage import current_bot_id_var
from src.infrastructure.database.models.dto.mirror_bot import MirrorBotDto


class MirrorBotManager:
    """Manages mirror bot instances, webhooks, and update routing."""

    def __init__(self, dispatcher: Dispatcher, domain: SecretStr) -> None:
        self.dispatcher = dispatcher
        self.domain = domain
        self._bots: dict[int, Bot] = {}  # mirror_bot_id -> Bot instance
        self._secrets: dict[int, str] = {}  # mirror_bot_id -> secret token
        self._feed_tasks: set[asyncio.Task[Any]] = set()

    @property
    def active_bots(self) -> dict[int, Bot]:
        return dict(self._bots)

    async def start_mirror_bot(self, mirror_bot: MirrorBotDto, allowed_updates: list[str]) -> bool:
        """Start a mirror bot: create Bot instance, set webhook."""
        if mirror_bot.id in self._bots:
            logger.debug(f"Mirror bot @{mirror_bot.username} already running")
            return True

        try:
            bot = Bot(
                token=mirror_bot.token,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            )

            # Verify the token is valid
            bot_info = await bot.get_me()
            logger.info(f"Mirror bot @{bot_info.username} (id={bot_info.id}) validated")

            # Generate a unique secret token for this mirror bot
            secret_token = secrets.token_hex(32)

            # Set webhook
            webhook_path = self._get_webhook_path(mirror_bot.id)
            webhook_url = f"https://{self.domain.get_secret_value()}{webhook_path}"

            webhook = SetWebhook(
                url=webhook_url,
                allowed_updates=allowed_updates,
                drop_pending_updates=True,
                secret_token=secret_token,
            )

            if not await bot(webhook):
                logger.error(f"Failed to set webhook for mirror bot @{mirror_bot.username}")
                await bot.session.close()
                return False

            self._bots[mirror_bot.id] = bot
            self._secrets[mirror_bot.id] = secret_token

            logger.success(f"Mirror bot @{mirror_bot.username} started with webhook: {webhook_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to start mirror bot @{mirror_bot.username}: {e}")
            return False

    async def stop_mirror_bot(self, mirror_bot_id: int) -> None:
        """Stop and cleanup a mirror bot."""
        bot = self._bots.pop(mirror_bot_id, None)
        self._secrets.pop(mirror_bot_id, None)

        if bot:
            try:
                await bot.delete_webhook()
            except Exception as e:
                logger.warning(f"Failed to delete webhook for mirror bot {mirror_bot_id}: {e}")
            try:
                await bot.session.close()
            except Exception:
                pass
            logger.info(f"Mirror bot {mirror_bot_id} stopped")

    async def stop_all(self) -> None:
        """Stop all mirror bots."""
        for mirror_id in list(self._bots.keys()):
            await self.stop_mirror_bot(mirror_id)

        # Cancel any pending feed tasks
        for task in list(self._feed_tasks):
            if not task.done():
                task.cancel()
        await asyncio.gather(*self._feed_tasks, return_exceptions=True)
        self._feed_tasks.clear()

    def register_routes(self, app: FastAPI) -> None:
        """Register webhook routes for mirror bots."""
        app.add_api_route(
            path="/api/v1/webhook/mirror/{mirror_id}",
            endpoint=self._handle_mirror_webhook,
            methods=["POST"],
        )
        logger.debug("Registered mirror bot webhook route")

    async def _handle_mirror_webhook(
        self,
        mirror_id: int,
        update: Annotated[Update, Body()],
        x_telegram_bot_api_secret_token: Annotated[str, Header()],
    ) -> Response:
        """Handle incoming webhook updates for mirror bots."""
        bot = self._bots.get(mirror_id)
        secret = self._secrets.get(mirror_id)

        if not bot or not secret:
            logger.warning(f"Received webhook for unknown mirror bot {mirror_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if not secrets.compare_digest(x_telegram_bot_api_secret_token, secret):
            logger.warning(f"Invalid secret token for mirror bot {mirror_id}, update {update.update_id}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        task = asyncio.create_task(self._feed_update(bot, update))
        self._feed_tasks.add(task)
        task.add_done_callback(self._feed_tasks.discard)

        return Response(status_code=status.HTTP_200_OK)

    async def _feed_update(self, bot: Bot, update: Update) -> None:
        """Feed an update from a mirror bot through the dispatcher."""
        _token = current_bot_id_var.set(bot.id)
        try:
            result = await self.dispatcher.feed_update(bot=bot, update=update)
            if isinstance(result, TelegramMethod):
                await self.dispatcher.silent_call_request(bot=bot, result=result)
        except Exception as e:
            logger.error(f"Error processing mirror bot update {update.update_id}: {e}")
        finally:
            current_bot_id_var.reset(_token)

    @staticmethod
    def _get_webhook_path(mirror_bot_id: int) -> str:
        return f"/api/v1/webhook/mirror/{mirror_bot_id}"
