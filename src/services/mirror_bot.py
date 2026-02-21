from typing import Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fluentogram import TranslatorHub
from loguru import logger
from redis.asyncio import Redis

from src.core.config import AppConfig
from src.core.security.crypto import decrypt, encrypt, is_encrypted
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto.mirror_bot import MirrorBotDto
from src.infrastructure.database.models.sql.mirror_bot import MirrorBot
from src.infrastructure.redis import RedisRepository

from .base import BaseService


class MirrorBotService(BaseService):
    """Service for managing mirror (additional) bots."""

    uow: UnitOfWork

    def __init__(
        self,
        config: AppConfig,
        bot: Bot,
        redis_client: Redis,
        redis_repository: RedisRepository,
        translator_hub: TranslatorHub,
        #
        uow: UnitOfWork,
    ) -> None:
        super().__init__(config, bot, redis_client, redis_repository, translator_hub)
        self.uow = uow

    async def get_all(self) -> list[MirrorBotDto]:
        """Get all mirror bots."""
        async with self.uow as uow:
            bots = await uow.repository.mirror_bots.get_all()
            return [self._to_dto(b) for b in bots]

    async def get_active(self) -> list[MirrorBotDto]:
        """Get all active mirror bots."""
        async with self.uow as uow:
            bots = await uow.repository.mirror_bots.get_active()
            return [self._to_dto(b) for b in bots]

    async def get(self, mirror_bot_id: int) -> Optional[MirrorBotDto]:
        """Get a mirror bot by ID."""
        async with self.uow as uow:
            bot = await uow.repository.mirror_bots.get(mirror_bot_id)
            return self._to_dto(bot) if bot else None

    async def add(self, token: str) -> MirrorBotDto:
        """
        Validate and add a new mirror bot.
        Raises ValueError if the token is invalid or bot already exists.
        """
        # Validate token by trying to create a bot and get info
        try:
            test_bot = Bot(
                token=token,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            )
            bot_info = await test_bot.get_me()
            username = bot_info.username or f"bot_{bot_info.id}"
            await test_bot.session.close()
        except Exception as e:
            raise ValueError(f"Невалидный токен бота: {e}") from e

        # Check if already exists
        encrypted_token = encrypt(token)
        async with self.uow as uow:
            existing = await uow.repository.mirror_bots.get_by_username(username)
            if existing:
                raise ValueError(f"Бот @{username} уже добавлен")

            mirror_bot = MirrorBot(
                token=encrypted_token,
                username=username,
                is_active=True,
            )
            created = await uow.repository.mirror_bots.create(mirror_bot)
            await uow.commit()
            logger.info(f"Added mirror bot @{username} (id={created.id})")
            return self._to_dto(created)

    async def get_primary(self) -> Optional[MirrorBotDto]:
        """Get the primary mirror bot (used for invite links), or None."""
        async with self.uow as uow:
            bot = await uow.repository.mirror_bots.get_primary()
            return self._to_dto(bot) if bot else None

    async def set_primary(self, mirror_bot_id: Optional[int]) -> None:
        """
        Set a mirror bot as primary for invite links.
        Pass None to clear the primary selection (use main bot).
        """
        async with self.uow as uow:
            await uow.repository.mirror_bots.unset_all_primary()
            if mirror_bot_id is not None:
                bot = await uow.repository.mirror_bots.get(mirror_bot_id)
                if bot:
                    bot.is_primary = True
            await uow.commit()

    async def remove(self, mirror_bot_id: int) -> Optional[str]:
        """Remove a mirror bot by ID. Returns the username or None."""
        async with self.uow as uow:
            bot = await uow.repository.mirror_bots.get(mirror_bot_id)
            if not bot:
                return None
            username = bot.username
            await uow.repository.mirror_bots.delete(bot)
            await uow.commit()
            logger.info(f"Removed mirror bot @{username} (id={mirror_bot_id})")
            return username

    def _to_dto(self, model: MirrorBot) -> MirrorBotDto:
        """Convert SQL model to DTO, decrypting token."""
        token = model.token
        if is_encrypted(token):
            token = decrypt(token)
        return MirrorBotDto(
            id=model.id,
            token=token,
            username=model.username,
            is_active=model.is_active,
            is_primary=model.is_primary,
        )

    @staticmethod
    async def validate_token(token: str) -> Optional[str]:
        """
        Validate a bot token and return the bot username.
        Returns None if invalid.
        """
        try:
            test_bot = Bot(
                token=token,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            )
            bot_info = await test_bot.get_me()
            username = bot_info.username
            await test_bot.session.close()
            return username
        except Exception:
            return None
