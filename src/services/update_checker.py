from typing import Optional

import httpx
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from src.__version__ import __version__
from src.core.constants import DEFAULT_BRANCH, REPOSITORY, get_update_branch
from src.core.enums import SystemNotificationType
from src.core.storage.keys import LastNotifiedVersionKey, UpdateSnoozeKey
from src.core.utils.message_payload import MessagePayload
from src.infrastructure.redis.repository import RedisRepository
from src.services.notification import NotificationService
from src.services.settings import SettingsService

from .base import BaseService

from aiogram import Bot
from fluentogram import TranslatorHub
from redis.asyncio import Redis
from src.core.config import AppConfig

# Raw URL для чтения .update напрямую с GitHub
_GITHUB_RAW_UPDATE_URL = (
    REPOSITORY.replace("github.com", "raw.githubusercontent.com") + "/{branch}/assets/update/.update"
)

# Callback data prefixes for update snooze buttons
UPDATE_SNOOZE_PREFIX = "update_snooze:"
UPDATE_SNOOZE_1D = f"{UPDATE_SNOOZE_PREFIX}1"
UPDATE_SNOOZE_3D = f"{UPDATE_SNOOZE_PREFIX}3"
UPDATE_SNOOZE_7D = f"{UPDATE_SNOOZE_PREFIX}7"
UPDATE_SNOOZE_OFF = f"{UPDATE_SNOOZE_PREFIX}off"
UPDATE_NOW = "update_now"
UPDATE_CLOSE = "update_close"


def _parse_version(version_str: str) -> tuple[int, ...]:
    """Parse version string like '0.4.6' into tuple (0, 4, 6) for comparison."""
    try:
        return tuple(int(x) for x in version_str.strip().split("."))
    except (ValueError, AttributeError):
        return (0, 0, 0)


class UpdateCheckerService(BaseService):
    notification_service: NotificationService
    settings_service: SettingsService

    def __init__(
        self,
        config: AppConfig,
        bot: Bot,
        redis_client: Redis,
        redis_repository: RedisRepository,
        translator_hub: TranslatorHub,
        #
        notification_service: NotificationService,
        settings_service: SettingsService,
    ) -> None:
        super().__init__(config, bot, redis_client, redis_repository, translator_hub)
        self.notification_service = notification_service
        self.settings_service = settings_service

    async def _fetch_remote_version(self, branch: str = DEFAULT_BRANCH) -> Optional[str]:
        """Fetch the latest version from GitHub."""
        url = _GITHUB_RAW_UPDATE_URL.format(branch=branch)
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                for line in response.text.splitlines():
                    if line.startswith("version:"):
                        return line.split(":", 1)[1].strip()
                return None
        except Exception as e:
            logger.warning(f"[update_checker] Failed to fetch remote version: {e}")
            return None

    async def _get_last_notified_version(self) -> Optional[str]:
        """Get the last version we already notified about from Redis."""
        key = LastNotifiedVersionKey()
        return await self.redis_repository.get(key, str)

    async def _set_last_notified_version(self, version: str) -> None:
        """Save the last notified version to Redis."""
        key = LastNotifiedVersionKey()
        await self.redis_repository.set(key, version)

    async def is_snoozed(self) -> bool:
        """Check if update notifications are currently snoozed."""
        key = UpdateSnoozeKey()
        value = await self.redis_repository.get(key, str)
        return value is not None

    async def set_snooze(self, days: int) -> None:
        """Snooze update notifications for N days."""
        key = UpdateSnoozeKey()
        ex = days * 86400  # days to seconds
        await self.redis_repository.set(key, "1", ex=ex)
        logger.info(f"[update_checker] Snoozed update notifications for {days} day(s)")

    async def disable_notifications(self) -> None:
        """Disable update notifications permanently (until new version appears)."""
        key = UpdateSnoozeKey()
        # Set for 365 days — effectively permanent until a new version resets it
        await self.redis_repository.set(key, "permanent", ex=365 * 86400)
        logger.info("[update_checker] Update notifications disabled permanently")

    async def _clear_snooze_for_new_version(self, version: str) -> None:
        """Clear snooze if a newer version than the snoozed one appeared."""
        last_notified = await self._get_last_notified_version()
        if last_notified and _parse_version(version) > _parse_version(last_notified):
            # New version appeared — reset snooze
            key = UpdateSnoozeKey()
            await self.redis_repository.delete(key)
            logger.info(f"[update_checker] Cleared snooze — new version {version} detected")

    def _build_snooze_keyboard(self) -> InlineKeyboardMarkup:
        """Build inline keyboard with update/snooze/dismiss buttons."""
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="btn-update-now", callback_data=UPDATE_NOW, style="primary"),
        )
        builder.row(
            InlineKeyboardButton(text="btn-update-remind-1d", callback_data=UPDATE_SNOOZE_1D),
            InlineKeyboardButton(text="btn-update-remind-3d", callback_data=UPDATE_SNOOZE_3D),
            InlineKeyboardButton(text="btn-update-remind-7d", callback_data=UPDATE_SNOOZE_7D),
        )
        builder.row(
            InlineKeyboardButton(text="btn-update-remind-off", callback_data=UPDATE_SNOOZE_OFF),
            InlineKeyboardButton(text="btn-update-close", callback_data=UPDATE_CLOSE, style="danger"),
        )
        return builder.as_markup()

    async def check_for_updates(self) -> None:
        """Check if a new version is available and notify the developer."""
        local_version = __version__
        branch = get_update_branch()
        remote_version = await self._fetch_remote_version(branch=branch)

        if not remote_version:
            logger.debug("[update_checker] Could not fetch remote version, skipping check")
            return

        local_parsed = _parse_version(local_version)
        remote_parsed = _parse_version(remote_version)

        if remote_parsed <= local_parsed:
            logger.debug(
                f"[update_checker] Bot is up to date (local={local_version}, remote={remote_version})"
            )
            return

        # Clear snooze if this is a brand-new version
        await self._clear_snooze_for_new_version(remote_version)

        # Check if notifications are snoozed
        if await self.is_snoozed():
            logger.debug("[update_checker] Update notifications are snoozed, skipping")
            return

        # Send notification to developer with snooze buttons
        logger.info(
            f"[update_checker] New version available: {remote_version} (current: {local_version})"
        )

        await self.notification_service.system_notify(
            payload=MessagePayload(
                i18n_key="ntf-system-update-available",
                i18n_kwargs={
                    "current_version": local_version,
                    "new_version": remote_version,
                },
                auto_delete_after=None,
                add_close_button=False,
                reply_markup=self._build_snooze_keyboard(),
            ),
            ntf_type=SystemNotificationType.BOT_UPDATE,
        )

        await self._set_last_notified_version(remote_version)
