from dataclasses import dataclass
from typing import TYPE_CHECKING, Annotated, NewType, Optional, TypeAlias, Union

from aiogram.types import (
    BufferedInputFile,
    ForceReply,
    FSInputFile,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from pydantic import PlainValidator
from remnapy.models import UserResponseDto
from remnapy.models.webhook import UserDto as UserWebhookDto

from src.core.enums import Locale, SystemNotificationType, UserNotificationType


@dataclass(frozen=True, slots=True)
class CreateUserInput:
    """Platform-agnostic input for user creation.

    Can be constructed from any source: Telegram Bot, Mini App, Website, etc.
    """

    telegram_id: int
    full_name: str
    username: Optional[str] = None
    language_code: Optional[str] = None

if TYPE_CHECKING:
    ListStr: TypeAlias = list[str]
    ListLocale: TypeAlias = list[Locale]
else:
    ListStr = NewType("ListStr", list[str])
    ListLocale = NewType("ListLocale", list[Locale])

AnyInputFile: TypeAlias = Union[BufferedInputFile, FSInputFile]

AnyKeyboard: TypeAlias = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
]

AnyNotification: TypeAlias = Union[SystemNotificationType, UserNotificationType]

RemnaUserDto: TypeAlias = Union[UserWebhookDto, UserResponseDto]  # UserWebhookDto without url

StringList: TypeAlias = Annotated[
    ListStr, PlainValidator(lambda x: [s.strip() for s in x.split(",")])
]
LocaleList: TypeAlias = Annotated[
    ListLocale, PlainValidator(func=lambda x: [Locale(loc.strip()) for loc in x.split(",")])
]
