from typing import Any, Optional, Union

from aiogram_dialog.api.internal import TextWidget
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from dishka import AsyncContainer
from fluentogram import TranslatorRunner
from magic_filter import MagicFilter

from src.core.constants import CONTAINER_KEY
from src.core.i18n.translator import get_translated_kwargs
from src.core.utils.formatters import i18n_postprocess_text


def default_format_text(text: str, data: dict[str, Any]) -> str:
    return text.format_map(data)


class I18nFormat(Text):
    def __init__(
        self,
        key: str,
        when: Optional[WhenCondition] = None,
        /,
        **mapping: Union[TextWidget, MagicFilter, str, int, float, bool],
    ) -> None:
        super().__init__(when)
        self.key = key
        self.mapping = mapping

    async def _transform(
        self,
        data: dict[str, Any],
        dialog_manager: DialogManager,
    ) -> dict[str, Any]:
        mapped: dict[str, Any] = {}

        for key, transformer in self.mapping.items():
            if isinstance(transformer, TextWidget):
                mapped[key] = await transformer.render_text(data, dialog_manager)
            elif isinstance(transformer, MagicFilter):
                mapped[key] = transformer.resolve(data)
            else:
                mapped[key] = transformer

        return {**data, **mapped}

    async def _render_text(self, data: dict[str, Any], dialog_manager: DialogManager) -> str:
        # Проверяем, есть ли переопределенный translator_runner в middleware_data
        # (используется для временного переключения языка)
        i18n: Optional[TranslatorRunner] = dialog_manager.middleware_data.get("translator_runner")
        
        if i18n is None:
            # Если нет переопределения, получаем стандартный из контейнера
            container: AsyncContainer = dialog_manager.middleware_data[CONTAINER_KEY]
            i18n = await container.get(TranslatorRunner)

        if self.mapping:
            data = await self._transform(data, dialog_manager)

        data = get_translated_kwargs(i18n, data)
        translated_text = i18n.get(self.key.format_map(data), **data)
        return i18n_postprocess_text(text=translated_text)
