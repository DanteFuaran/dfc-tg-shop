from typing import Any, Optional

from src.infrastructure.database.models.sql import Settings

from .base import BaseRepository


class SettingsRepository(BaseRepository):
    async def create(self, settings: Settings) -> Settings:
        return await self.create_instance(settings)

    async def get(self) -> Optional[Settings]:
        return await self._get_one(Settings)

    async def update(self, **data: Any) -> Optional[Settings]:
        # Всегда обновляем первую (и единственную) запись настроек
        existing = await self._get_one(Settings)
        if existing is None:
            # Если настроек нет, возвращаем None и позволяем создать новые
            return None
        return await self._update(Settings, Settings.id == existing.id, **data)
