from typing import Optional

from sqlalchemy import func

from src.infrastructure.database.models.sql.web_credential import WebCredential

from .base import BaseRepository


class WebCredentialRepository(BaseRepository):
    async def create(self, credential: WebCredential) -> WebCredential:
        return await self.create_instance(credential)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[WebCredential]:
        return await self._get_one(WebCredential, WebCredential.telegram_id == telegram_id)

    async def get_by_username(self, web_username: str) -> Optional[WebCredential]:
        return await self._get_one(
            WebCredential,
            func.lower(WebCredential.web_username) == web_username.lower(),
        )

    async def update_password(self, telegram_id: int, password_hash: str) -> Optional[WebCredential]:
        return await self._update(
            WebCredential,
            WebCredential.telegram_id == telegram_id,
            password_hash=password_hash,
        )

    async def delete(self, telegram_id: int) -> bool:
        return bool(
            await self._delete(WebCredential, WebCredential.telegram_id == telegram_id)
        )
