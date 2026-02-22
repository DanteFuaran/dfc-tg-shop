from typing import Optional

from pydantic import Field

from .base import TrackableDto


class WebCredentialDto(TrackableDto):
    id: Optional[int] = Field(default=None, frozen=True)
    telegram_id: int
    web_username: str
    password_hash: str
