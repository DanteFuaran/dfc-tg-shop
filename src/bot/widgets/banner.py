from pathlib import Path
from typing import Any, Optional

from aiogram.types import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.media import StaticMedia
from loguru import logger

from src.core.config import AppConfig
from src.core.constants import CONFIG_KEY
from src.core.enums import BannerFormat


def get_banner(banners_dir: Path) -> tuple[Path, ContentType] | None:
    for fmt in BannerFormat:
        candidate = banners_dir / f"default.{fmt}"
        if candidate.exists():
            return candidate, fmt.content_type
    logger.warning(f"Default banner not found in '{banners_dir}'")
    return None


class Banner(StaticMedia):
    def __init__(self) -> None:
        def _is_use_banners(
            data: dict[str, Any],
            widget: Whenable,
            dialog_manager: DialogManager,
        ) -> bool:
            config: AppConfig = dialog_manager.middleware_data[CONFIG_KEY]
            return config.bot.use_banners

        super().__init__(path="path", url=None, type=ContentType.UNKNOWN, when=_is_use_banners)

    async def _render_media(self, data: dict, manager: DialogManager) -> Optional[MediaAttachment]:
        config: AppConfig = manager.middleware_data[CONFIG_KEY]

        result = get_banner(banners_dir=config.banners_dir)
        if result is None:
            return None

        banner_path, banner_content_type = result

        return MediaAttachment(
            type=banner_content_type,
            url=None,
            path=banner_path,
            use_pipe=self.use_pipe,
            **self.media_params,
        )
