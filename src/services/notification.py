import asyncio
import uuid
from typing import Any, ClassVar, Optional, Union, cast

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import (
    BufferedInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorHub
from loguru import logger
from redis.asyncio import Redis

from src.__version__ import __version__
from src.bot.keyboards import get_remnashop_keyboard
from src.bot.states import Notification
from src.core.config import AppConfig
from src.core.constants import REPOSITORY
from src.core.enums import (
    Locale,
    MediaType,
    MessageEffect,
    SystemNotificationType,
    UserNotificationType,
    UserRole,
)
from src.core.i18n.translator import get_translated_kwargs
from src.core.utils.formatters import i18n_postprocess_text
from src.core.utils.message_payload import MessagePayload
from src.core.utils.types import AnyKeyboard
from src.infrastructure.database.models.dto import UserDto
from src.infrastructure.database.models.dto.user import BaseUserDto
from src.infrastructure.redis.repository import RedisRepository
from src.services.settings import SettingsService

from .base import BaseService
from .user import UserService


class NotificationService(BaseService):
    # Module-level singleton for the mirror bot manager.
    # Set once during app startup via set_mirror_bot_manager().
    _mirror_bot_manager: ClassVar[Optional[Any]] = None  # type: MirrorBotManager

    @classmethod
    def set_mirror_bot_manager(cls, manager: Optional[Any]) -> None:  # type: MirrorBotManager
        """Register the active MirrorBotManager so notifications reach all bots."""
        cls._mirror_bot_manager = manager
        count = len(manager.active_bots) if manager else 0
        logger.info(f"NotificationService: mirror bot manager set ({count} active mirror bots)")

    user_service: UserService
    settings_service: SettingsService

    def __init__(
        self,
        config: AppConfig,
        bot: Bot,
        redis_client: Redis,
        redis_repository: RedisRepository,
        translator_hub: TranslatorHub,
        #
        user_service: UserService,
        settings_service: SettingsService,
    ) -> None:
        super().__init__(config, bot, redis_client, redis_repository, translator_hub)
        self.user_service = user_service
        self.settings_service = settings_service

    async def notify_user(
        self,
        user: Optional[BaseUserDto],
        payload: MessagePayload,
        ntf_type: Optional[UserNotificationType] = None,
    ) -> Optional[Message]:
        if not user:
            logger.warning("Skipping user notification: user object is empty")
            return None

        # Проверяем глобальное включение уведомлений
        settings = await self.settings_service.get()
        if not settings.features.notifications_enabled:
            logger.debug(
                f"Skipping user notification for '{user.telegram_id}': "
                f"global notifications are disabled in settings"
            )
            return None

        if ntf_type and not await self.settings_service.is_notification_enabled(ntf_type):
            logger.debug(
                f"Skipping user notification for '{user.telegram_id}': "
                f"notification type is disabled in settings"
            )
            return None

        logger.debug(
            f"Attempting to send user notification '{payload.i18n_key}' to '{user.telegram_id}'"
        )

        # Определяем язык уведомления в зависимости от настройки мультиязычности
        if settings.features.language_enabled:
            # Мультиязычность включена - используем язык пользователя
            locale_override = user.language
            logger.debug(
                f"Using user language '{locale_override}' for user '{user.telegram_id}' (multilingual mode)"
            )
        else:
            # Мультиязычность выключена - используем язык админа
            locale_override = settings.bot_locale
            logger.debug(
                f"Using bot_locale '{locale_override}' for user '{user.telegram_id}'"
            )

        return await self._send_message(user, payload, locale_override=locale_override)

    async def system_notify(
        self,
        payload: MessagePayload,
        ntf_type: SystemNotificationType,
    ) -> list[bool]:
        devs = await self.user_service.get_by_role(role=UserRole.DEV)

        if not devs:
            devs = [self._get_temp_dev()]

        if not await self.settings_service.is_notification_enabled(ntf_type):
            logger.debug("Skipping system notification: notification type is disabled in settings")
            return []

        settings = await self.settings_service.get()

        logger.debug(
            f"Attempting to send system notification '{payload.i18n_key}' to '{len(devs)}' devs"
        )

        async def send_to_dev(dev: UserDto) -> bool:
            # Определяем язык в зависимости от мультиязычности
            if settings.features.language_enabled:
                # Мультиязычность включена - используем язык dev пользователя
                locale = dev.language
            else:
                # Мультиязычность выключена - используем bot_locale
                locale = settings.bot_locale
            return bool(await self._send_message(user=dev, payload=payload, locale_override=locale))

        tasks = [send_to_dev(dev) for dev in devs]
        results = await asyncio.gather(*tasks)

        return cast(list[bool], results)

    async def notify_super_dev(self, payload: MessagePayload) -> bool:
        dev = await self.user_service.get(telegram_id=self.config.bot.dev_id)

        if not dev:
            dev = self._get_temp_dev()

        settings = await self.settings_service.get()
        
        # Определяем язык в зависимости от мультиязычности
        if settings.features.language_enabled:
            # Мультиязычность включена - используем язык dev пользователя
            locale = dev.language
        else:
            # Мультиязычность выключена - используем bot_locale
            locale = settings.bot_locale

        logger.debug(
            f"Attempting to send super dev notification '{payload.i18n_key}' to '{dev.telegram_id}' (locale: {locale})"
        )

        return bool(await self._send_message(user=dev, payload=payload, locale_override=locale))

    async def error_notify(
        self,
        traceback_str: str,
        payload: MessagePayload,
        error_id: Optional[Union[str, int]] = str(uuid.uuid4()),
    ) -> None:
        file_data = BufferedInputFile(
            file=traceback_str.encode(),
            filename=f"error_{error_id}.txt",
        )
        payload.media = file_data
        payload.media_type = MediaType.DOCUMENT
        payload.i18n_kwargs.update(self.config.build.data)
        await self.notify_super_dev(payload=payload)

    #

    async def _send_message(
        self,
        user: BaseUserDto,
        payload: MessagePayload,
        locale_override: Optional[Locale] = None,
    ) -> Optional[Message]:
        # Используем переопределённую локаль или язык пользователя
        locale = locale_override or user.language
        
        reply_markup = self._prepare_reply_markup(
            payload.reply_markup,
            payload.add_close_button,
            payload.auto_delete_after,
            locale,
            user.telegram_id,
            payload.close_button_style,
        )
        try:
            if (payload.media or payload.media_id) and payload.media_type:
                sent_message = await self._send_media_message(user, payload, reply_markup, locale)
            else:
                if (payload.media or payload.media_id) and not payload.media_type:
                    logger.warning(
                        f"Validation warning: Media provided without media_type "
                        f"for chat '{user.telegram_id}'. Sending as text message"
                    )
                sent_message = await self._send_text_message(user, payload, reply_markup, locale)

            if payload.auto_delete_after is not None and sent_message:
                asyncio.create_task(
                    self._schedule_message_deletion(
                        chat_id=user.telegram_id,
                        message_id=sent_message.message_id,
                        delay=payload.auto_delete_after,
                    )
                )

            # Track closeable messages in Redis for auto-cleanup after 45h
            if (
                payload.add_close_button
                and payload.auto_delete_after is None
                and sent_message
            ):
                await self._track_closeable_message(
                    chat_id=user.telegram_id,
                    message_id=sent_message.message_id,
                )

            # ── Also send via any active mirror bots ───────────────────
            if self._mirror_bot_manager:
                for mirror_bot in self._mirror_bot_manager.active_bots.values():
                    try:
                        if (payload.media or payload.media_id) and payload.media_type:
                            mirror_sent = await self._send_media_message(user, payload, reply_markup, locale, bot=mirror_bot)
                        else:
                            mirror_sent = await self._send_text_message(user, payload, reply_markup, locale, bot=mirror_bot)
                        # Schedule auto-deletion for the mirror bot message using its own bot instance
                        if payload.auto_delete_after is not None and mirror_sent:
                            asyncio.create_task(
                                self._schedule_message_deletion(
                                    chat_id=user.telegram_id,
                                    message_id=mirror_sent.message_id,
                                    delay=payload.auto_delete_after,
                                    bot=mirror_bot,
                                )
                            )
                    except (TelegramBadRequest, TelegramForbiddenError):
                        pass  # User never started this mirror bot — expected
                    except Exception as e:
                        logger.debug(f"Mirror bot {mirror_bot.id}: notification to {user.telegram_id} skipped: {e}")

            return sent_message

        except TelegramBadRequest as exception:
            if "chat not found" in str(exception).lower():
                logger.warning(
                    f"Chat not found for user '{user.telegram_id}'. "
                    f"User may have deleted the chat or blocked the bot."
                )
            else:
                logger.exception(
                    f"Bad request sending notification '{payload.i18n_key}' "
                    f"to '{user.telegram_id}': {exception}"
                )
            return None
        except TelegramForbiddenError as exception:
            logger.warning(
                f"User '{user.telegram_id}' blocked the bot. "
                f"Cannot send notification '{payload.i18n_key}'"
            )
            return None
        except TelegramRetryAfter as exception:
            logger.warning(
                f"Telegram rate limit for '{payload.i18n_key}' "
                f"to '{user.telegram_id}'. Retry after {exception.retry_after}s"
            )
            return None

    async def _send_media_message(
        self,
        user: BaseUserDto,
        payload: MessagePayload,
        reply_markup: Optional[AnyKeyboard],
        locale: Optional[Locale] = None,
        bot: Optional[Bot] = None,
    ) -> Message:
        message_text = self._get_translated_text(
            locale=locale or user.language,
            i18n_key=payload.i18n_key,
            i18n_kwargs=payload.i18n_kwargs,
        )

        assert payload.media_type
        _bot = bot or self.bot
        send_func = payload.media_type.get_function(_bot)
        media_arg_name = payload.media_type.lower()

        media_input = payload.media or payload.media_id
        if media_input is None:
            raise ValueError(f"Missing media content for {payload.media_type}")

        tg_payload = {
            "chat_id": user.telegram_id,
            "caption": message_text,
            "reply_markup": reply_markup,
            "message_effect_id": payload.message_effect,
            media_arg_name: media_input,
        }
        return cast(Message, await send_func(**tg_payload))

    async def _send_text_message(
        self,
        user: BaseUserDto,
        payload: MessagePayload,
        reply_markup: Optional[AnyKeyboard],
        locale: Optional[Locale] = None,
        bot: Optional[Bot] = None,
    ) -> Message:
        # Используем raw text если он предоставлен, иначе переводим i18n ключ
        effective_locale = locale or user.language
        if payload.text:
            message_text = payload.text
        elif payload.i18n_key:
            message_text = self._get_translated_text(
                locale=effective_locale,
                i18n_key=payload.i18n_key,
                i18n_kwargs=payload.i18n_kwargs,
            )
        else:
            raise ValueError("Either 'text' or 'i18n_key' must be provided in MessagePayload")

        _bot = bot or self.bot
        return await _bot.send_message(
            chat_id=user.telegram_id,
            text=message_text,
            message_effect_id=payload.message_effect,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )

    def _prepare_reply_markup(
        self,
        reply_markup: Optional[AnyKeyboard],
        add_close_button: bool,
        auto_delete_after: Optional[int],
        locale: Locale,
        chat_id: int,
        close_button_style: str = "danger",
    ) -> Optional[AnyKeyboard]:
        if reply_markup is None:
            if add_close_button and auto_delete_after is None:
                close_button = self._get_close_notification_button(locale=locale, style=close_button_style)
                return self._get_close_notification_keyboard(close_button)
            return None

        if not add_close_button or auto_delete_after is not None:
            return self._translate_keyboard_texts(reply_markup, locale)

        close_button = self._get_close_notification_button(locale=locale, style=close_button_style)

        if isinstance(reply_markup, InlineKeyboardMarkup):
            translated_markup = self._translate_keyboard_texts(reply_markup, locale)
            translated_markup = cast(InlineKeyboardMarkup, translated_markup)
            builder = InlineKeyboardBuilder.from_markup(translated_markup)
            builder.row(close_button)
            return builder.as_markup()

        if isinstance(reply_markup, ReplyKeyboardMarkup):
            return self._translate_keyboard_texts(reply_markup, locale)

        logger.warning(
            f"Unsupported reply_markup type '{type(reply_markup).__name__}' "
            f"for chat '{chat_id}'. Close button will not be added"
        )
        return reply_markup

    def _get_close_notification_button(self, locale: Locale, style: str = "danger") -> InlineKeyboardButton:
        i18n = self.translator_hub.get_translator_by_locale(locale=locale)
        i18n_key = "btn-notification-close-success" if style == "success" else "btn-notification-close"
        button_text = i18n.get(i18n_key)
        return InlineKeyboardButton(text=button_text, callback_data=Notification.CLOSE.state, style=style)

    def _get_close_notification_keyboard(
        self,
        button: InlineKeyboardButton,
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(button)
        return builder.as_markup()

    async def _track_closeable_message(self, chat_id: int, message_id: int) -> None:
        """Save message reference in Redis sorted set for auto-cleanup."""
        import time
        from src.core.storage.keys import CloseableMessagesKey

        key = CloseableMessagesKey()
        member = f"{chat_id}:{message_id}"
        await self.redis_repository.sorted_collection_add(
            key, {member: time.time()}
        )
        logger.debug(
            f"Tracked closeable message '{message_id}' in chat '{chat_id}'"
        )

    async def untrack_closeable_message(self, chat_id: int, message_id: int) -> None:
        """Remove message from closeable tracking (called when user clicks Close)."""
        from src.core.storage.keys import CloseableMessagesKey

        key = CloseableMessagesKey()
        member = f"{chat_id}:{message_id}"
        await self.redis_repository.sorted_collection_remove(key, member)

    async def _schedule_message_deletion(
        self,
        chat_id: int,
        message_id: int,
        delay: int,
        bot: Optional[Bot] = None,
    ) -> None:
        _bot = bot or self.bot
        logger.debug(
            f"Scheduling message '{message_id}' for auto-deletion in '{delay}' (chat '{chat_id}', bot={_bot.id})"
        )
        try:
            await asyncio.sleep(delay)
            await _bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.debug(
                f"Message '{message_id}' in chat '{chat_id}' deleted after '{delay}' seconds"
            )
        except Exception as exception:
            logger.error(
                f"Failed to delete message '{message_id}' in chat '{chat_id}': {exception}"
            )

    def _get_translated_text(
        self,
        locale: Locale,
        i18n_key: str,
        i18n_kwargs: dict[str, Any] = {},
    ) -> str:
        if not i18n_key:
            return i18n_key

        i18n = self.translator_hub.get_translator_by_locale(locale=locale)
        kwargs = get_translated_kwargs(i18n, i18n_kwargs)
        return i18n_postprocess_text(i18n.get(i18n_key, **kwargs))

    def _translate_keyboard_texts(self, keyboard: AnyKeyboard, locale: Locale) -> AnyKeyboard:  # noqa: C901
        if isinstance(keyboard, InlineKeyboardMarkup):
            new_inline_keyboard = []

            for row_inline in keyboard.inline_keyboard:
                new_row_inline = []
                for button_inline in row_inline:
                    if button_inline.text:
                        try:
                            button_inline.text = self._get_translated_text(
                                locale, button_inline.text
                            )
                        except Exception:
                            button_inline.text = button_inline.text
                    new_row_inline.append(button_inline)
                new_inline_keyboard.append(new_row_inline)

            return InlineKeyboardMarkup(inline_keyboard=new_inline_keyboard)

        elif isinstance(keyboard, ReplyKeyboardMarkup):
            new_keyboard = []

            for row in keyboard.keyboard:
                new_row = []
                for button in row:
                    if button.text:
                        try:
                            button.text = self._get_translated_text(locale, button.text)
                        except Exception:
                            button.text = button.text
                    new_row.append(button)
                new_keyboard.append(new_row)

            return ReplyKeyboardMarkup(
                keyboard=new_keyboard, **keyboard.model_dump(exclude={"keyboard"})
            )

        return keyboard

    def _get_temp_dev(self) -> UserDto:
        temp_dev = UserDto(
            telegram_id=self.config.bot.dev_id,
            name="TempDev",
            role=UserRole.DEV,
        )

        logger.warning("Fallback to temporary dev user from environment for notifications")
        return temp_dev
