from typing import Optional

from sqlalchemy import select, update

from src.infrastructure.database.models.sql.mirror_bot import MirrorBot

from .base import BaseRepository


class MirrorBotRepository(BaseRepository):
    async def get(self, mirror_bot_id: int) -> Optional[MirrorBot]:
        return await self._get_one(MirrorBot, MirrorBot.id == mirror_bot_id)

    async def get_by_token(self, token: str) -> Optional[MirrorBot]:
        return await self._get_one(MirrorBot, MirrorBot.token == token)

    async def get_by_username(self, username: str) -> Optional[MirrorBot]:
        return await self._get_one(MirrorBot, MirrorBot.username == username)

    async def get_all(self) -> list[MirrorBot]:
        return await self._get_many(MirrorBot, order_by=MirrorBot.id)

    async def get_active(self) -> list[MirrorBot]:
        return await self._get_many(
            MirrorBot,
            MirrorBot.is_active == True,  # noqa: E712
            order_by=MirrorBot.id,
        )

    async def get_primary(self) -> Optional[MirrorBot]:
        """Return the bot marked as primary, or None."""
        return await self._get_one(MirrorBot, MirrorBot.is_primary == True)  # noqa: E712

    async def unset_all_primary(self) -> None:
        """Clear is_primary on all mirror bots."""
        await self.session.execute(update(MirrorBot).values(is_primary=False))

    async def create(self, mirror_bot: MirrorBot) -> MirrorBot:
        return await self.create_instance(mirror_bot)

    async def delete(self, mirror_bot: MirrorBot) -> None:
        await self.delete_instance(mirror_bot)

