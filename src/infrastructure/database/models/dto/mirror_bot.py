from typing import Optional

from .base import BaseDto


class MirrorBotDto(BaseDto):
    id: Optional[int] = None
    token: str
    username: str
    is_active: bool = True
