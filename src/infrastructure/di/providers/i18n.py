from typing import Optional

from dishka import Provider, Scope, provide
from dishka.integrations.aiogram import AiogramMiddlewareData
from fluentogram import TranslatorHub, TranslatorRunner
from fluentogram.storage import FileStorage
from loguru import logger

from src.core.config import AppConfig
from src.core.constants import USER_KEY, SETTINGS_KEY
from src.core.enums import Locale
from src.infrastructure.database.models.dto import UserDto, SettingsDto


class I18nProvider(Provider):
    scope = Scope.APP

    @provide
    def get_hub(self, config: AppConfig) -> TranslatorHub:
        storage = FileStorage(path=config.translations_dir / "{locale}")
        locales_map: dict[str, tuple[str, ...]] = {}

        for locale_code in config.locales:
            fallback_chain: list[str] = [locale_code]
            if config.default_locale != locale_code:
                fallback_chain.append(config.default_locale)
            locales_map[locale_code] = tuple(fallback_chain)

        if config.default_locale not in locales_map:
            locales_map[config.default_locale] = tuple(
                config.default_locale,
            )

        logger.debug(
            f"Loaded TranslatorHub with locales: "
            f"{[locale.value for locale in locales_map.keys()]}, "  # type: ignore[attr-defined]
            f"default={config.default_locale.value}"
        )

        return TranslatorHub(locales_map, root_locale=config.default_locale, storage=storage)

    @provide(scope=Scope.REQUEST)
    def get_translator(
        self,
        config: AppConfig,
        hub: TranslatorHub,
        middleware_data: AiogramMiddlewareData,
    ) -> TranslatorRunner:
        from fluentogram import TranslatorRunner
        
        # Сначала проверяем, есть ли переопределенный translator_runner 
        # (используется для временного переключения языка в настройках)
        override_translator: Optional[TranslatorRunner] = middleware_data.get("translator_runner")
        if override_translator is not None:
            return override_translator
        
        settings: Optional[SettingsDto] = middleware_data.get(SETTINGS_KEY)
        user: Optional[UserDto] = middleware_data.get(USER_KEY)

        # Определяем язык в зависимости от настройки мультиязычности
        if settings and settings.features.language_enabled and user:
            # Мультиязычность включена - используем язык пользователя (из Telegram)
            locale = user.language
        elif settings:
            # Мультиязычность выключена - используем глобальный язык админа
            locale = settings.bot_locale
        else:
            # Настройки не загружены - используем дефолтную локаль
            locale = config.default_locale

        return hub.get_translator_by_locale(locale=locale)
