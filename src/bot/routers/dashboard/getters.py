from typing import Any

import httpx
from aiogram_dialog import DialogManager
from loguru import logger

from src.__version__ import __version__
from src.core.config import AppConfig
from src.core.constants import DEFAULT_BRANCH, REPOSITORY, get_update_branch


def _build_version_url(branch: str) -> str:
    return REPOSITORY.replace("github.com", "raw.githubusercontent.com") + f"/{branch}/assets/update/.update"


def _parse_version(version_str: str) -> tuple[int, ...]:
    try:
        return tuple(int(x) for x in version_str.strip().split("."))
    except (ValueError, AttributeError):
        return (0, 0, 0)


async def _check_remote_version(branch: str = DEFAULT_BRANCH) -> tuple[bool, str]:
    """Check if a newer version is available. Returns (is_available, remote_version)."""
    try:
        url = _build_version_url(branch)
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            remote = ""
            for line in response.text.splitlines():
                if line.startswith("version:"):
                    remote = line.split(":", 1)[1].strip()
                    break
            if remote and _parse_version(remote) > _parse_version(__version__):
                return True, remote
    except Exception as e:
        logger.debug(f"[dashboard_getter] Failed to check remote version: {e}")
    return False, ""


async def dashboard_main_getter(
    dialog_manager: DialogManager,
    config: AppConfig,
    **kwargs: Any,
) -> dict[str, Any]:
    """Getter for dashboard main page."""
    branch = get_update_branch()
    update_available, new_version = await _check_remote_version(branch=branch)

    return {
        "bot_version": __version__,
        "update_available": "1" if update_available else "0",
        "new_version": new_version or __version__,
    }
