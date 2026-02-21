"""
Bot-aware MediaIdStorage for aiogram-dialog.

Problem: The default MediaIdStorage is an in-memory LRU cache keyed by
(path, url, content_type). It is shared across ALL bot instances in the process.
When the main bot uploads a banner (file_id X1), that file_id is stored in the
shared cache. When a mirror bot looks up the same path, it gets X1 — but X1 is
invalid for the mirror bot token. Telegram rejects it with
"Bad Request: wrong file identifier/HTTP URL specified".

Solution: Use a per-bot LRU cache. A ContextVar is set to the current bot_id
before each update is fed through the dispatcher. The BotAwareMediaIdStorage
reads this ContextVar to select the correct per-bot cache.

Usage:
  1. Import current_bot_id_var and BotAwareMediaIdStorage.
  2. Pass BotAwareMediaIdStorage() to setup_dialogs(media_id_storage=...).
  3. In each _feed_update(bot, update): set current_bot_id_var before feeding.
"""

import contextvars
from typing import Optional

from aiogram_dialog.setup import MediaIdStorage

# Set this contextvar to the current bot.id before calling dispatcher.feed_update
current_bot_id_var: contextvars.ContextVar[Optional[int]] = contextvars.ContextVar(
    "current_bot_id", default=None
)


class BotAwareMediaIdStorage:
    """
    MediaIdStorage that maintains separate LRU caches for each bot (by bot.id).

    This prevents mirror bots from using file_ids cached by the main bot,
    which would cause Telegram to return "wrong file identifier" errors.
    """

    def __init__(self, maxsize: int = 10240) -> None:
        self._maxsize = maxsize
        # Each bot gets its own MediaIdStorage instance (and its own LRU cache)
        self._storages: dict[int, MediaIdStorage] = {}

    def _get_storage(self) -> MediaIdStorage:
        bot_id = current_bot_id_var.get()
        # Fallback key 0 means "unknown bot" — safe default
        key = bot_id if bot_id is not None else 0
        if key not in self._storages:
            self._storages[key] = MediaIdStorage(self._maxsize)
        return self._storages[key]

    async def get_media_id(self, path, url, type):  # type: ignore[override]
        return await self._get_storage().get_media_id(path=path, url=url, type=type)

    async def save_media_id(self, path, url, type, media_id):  # type: ignore[override]
        await self._get_storage().save_media_id(path=path, url=url, type=type, media_id=media_id)
