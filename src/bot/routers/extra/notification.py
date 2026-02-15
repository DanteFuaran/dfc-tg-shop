import asyncio
import time
from typing import cast

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from loguru import logger

from src.bot.states import Notification
from src.core.constants import REPOSITORY, get_update_branch
from src.core.utils.formatters import format_user_log as log
from src.infrastructure.database.models.dto import UserDto
from src.services.notification import NotificationService
from src.services.update_checker import (
    UPDATE_CLOSE,
    UPDATE_NOW,
    UPDATE_SNOOZE_PREFIX,
    UpdateCheckerService,
)

router = Router(name=__name__)

# Host project directory (matches install.sh PROJECT_DIR)
_HOST_PROJECT_DIR = "/opt/dfc-tg-shop"

# Track pending update confirmations: {user_id: (timestamp, warning_message_id)}
_update_confirmations: dict[int, tuple[float, int]] = {}


@router.callback_query(F.data.startswith(Notification.CLOSE.state))
@inject
async def on_close_notification(
    callback: CallbackQuery,
    bot: Bot,
    user: UserDto,
    notification_service: FromDishka[NotificationService],
) -> None:
    notification: Message = cast(Message, callback.message)
    notification_id = notification.message_id

    logger.info(f"{log(user)} Closed notification '{notification_id}'")

    # Remove from auto-cleanup tracking
    try:
        await notification_service.untrack_closeable_message(
            chat_id=notification.chat.id,
            message_id=notification_id,
        )
    except Exception:
        pass

    try:
        await notification.delete()
        await callback.answer()
        logger.debug(f"Notification '{notification_id}' for user '{user.telegram_id}' deleted")
    except Exception as exception:
        logger.error(f"Failed to delete notification '{notification_id}'. Exception: {exception}")

        try:
            logger.debug(f"Attempting to remove keyboard from notification '{notification_id}'")
            await bot.edit_message_reply_markup(
                chat_id=notification.chat.id,
                message_id=notification.message_id,
                reply_markup=None,
            )
            logger.debug(f"Keyboard removed from notification '{notification_id}'")
        except Exception as exception:
            logger.error(
                f"Failed to remove keyboard from notification '{notification_id}'. "
                f"Exception: {exception}"
            )


@router.callback_query(F.data == UPDATE_NOW)
@inject
async def on_update_now(
    callback: CallbackQuery,
    bot: Bot,
    user: UserDto,
    update_checker_service: FromDishka[UpdateCheckerService],
) -> None:
    """Handle 'Update now' button — trigger bot update via Docker."""
    import subprocess

    notification: Message = cast(Message, callback.message)
    user_id = user.telegram_id
    now = time.time()

    # Check if this is a confirmation (second click within 5 seconds)
    last_confirmation = _update_confirmations.get(user_id)
    if not last_confirmation or now - last_confirmation[0] >= 5:
        # First click — show warning as separate message below
        await callback.answer()
        warning_msg = await bot.send_message(
            chat_id=user_id,
            text="⚠️ <b>Бот будет перезагружен!</b>\n<i>Нажмите ещё раз для подтверждения.</i>",
            parse_mode="HTML",
        )
        _update_confirmations[user_id] = (now, warning_msg.message_id)
        click_ts = now

        async def _revert_warning() -> None:
            await asyncio.sleep(5)
            # Only delete if no second click happened
            if user_id in _update_confirmations and _update_confirmations[user_id][0] == click_ts:
                _update_confirmations.pop(user_id, None)
                try:
                    await bot.delete_message(
                        chat_id=user_id,
                        message_id=warning_msg.message_id,
                    )
                except Exception:
                    pass

        asyncio.create_task(_revert_warning())
        return

    # Second click within 5s — delete warning and proceed with update
    warning_message_id = last_confirmation[1]
    _update_confirmations.pop(user_id, None)
    try:
        await bot.delete_message(chat_id=user_id, message_id=warning_message_id)
    except Exception:
        pass
    logger.info(f"{log(user)} Triggered bot update via notification button")

    try:
        await callback.answer()

        # Replace notification with "updating" message
        try:
            await bot.edit_message_text(
                chat_id=notification.chat.id,
                message_id=notification.message_id,
                text=(
                    "<b>⏳ Запущен процесс обновления!</b>\n"
                    "<i>Бот будет перезапущен автоматически.</i>"
                ),
                parse_mode="HTML",
                reply_markup=None,
            )
        except Exception:
            pass

        # Save message reference to Redis so it can be deleted after restart
        from src.core.storage.keys import UpdateInProgressKey, UpdateMessageKey
        redis_repo = update_checker_service.redis_repository
        msg_ref = f"{notification.chat.id}:{notification.message_id}"
        await redis_repo.set(UpdateMessageKey(), msg_ref, ex=600)  # TTL 10 min
        await redis_repo.set(UpdateInProgressKey(), "1", ex=600)  # TTL 10 min

        # Get repo info from config
        repo_url = REPOSITORY + ".git"
        branch = get_update_branch()

        # Spawn updater container using docker:cli (git/docker pre-installed)
        # - Mounts docker socket (for docker build/compose)
        # - Mounts host project dir (for file updates)
        # - Clones repo, copies files, rebuilds and restarts
        update_script = (
            "set -e && "
            "apk add --no-cache git >/dev/null 2>&1 && "
            f"git clone -b {branch} --depth 1 {repo_url} /tmp/repo && "
            f"cp /tmp/repo/docker-compose.yml {_HOST_PROJECT_DIR}/ && "
            f"cp /tmp/repo/Dockerfile {_HOST_PROJECT_DIR}/ && "
            f"cp /tmp/repo/pyproject.toml {_HOST_PROJECT_DIR}/ && "
            f"cp /tmp/repo/uv.lock {_HOST_PROJECT_DIR}/ && "
            f"cp -r /tmp/repo/src {_HOST_PROJECT_DIR}/ && "
            f"cp -r /tmp/repo/scripts {_HOST_PROJECT_DIR}/ && "
            f"cp -r /tmp/repo/assets/translations {_HOST_PROJECT_DIR}/assets/ 2>/dev/null || true && "
            f"cp -r /tmp/repo/assets/update {_HOST_PROJECT_DIR}/assets/ 2>/dev/null || true && "
            f"cp /tmp/repo/assets/README.md {_HOST_PROJECT_DIR}/assets/ 2>/dev/null || true && "
            f"cd {_HOST_PROJECT_DIR} && "
            "docker build -t dfc-tg:local . && "
            "docker compose up -d && "
            "rm -rf /tmp/repo"
        )

        cmd = [
            "docker", "run", "--rm", "-d",
            "--name", "dfc-tg-updater",
            "-v", "/var/run/docker.sock:/var/run/docker.sock",
            "-v", f"{_HOST_PROJECT_DIR}:{_HOST_PROJECT_DIR}",
            "docker:cli", "sh", "-c", update_script,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            logger.info(f"[update] Updater container started: {result.stdout.strip()[:12]}")
            # Stop the current bot container immediately so updater can rebuild freely
            logger.info("[update] Stopping current container to free resources for rebuild...")
            subprocess.Popen(
                ["docker", "stop", "-t", "5", "dfc-tg"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            logger.error(f"[update] Failed to start updater: {result.stderr}")

    except Exception as e:
        logger.error(f"[update] Failed to trigger update: {e}")
        try:
            await callback.answer("❌ Ошибка запуска обновления", show_alert=True)
        except Exception:
            pass


@router.callback_query(F.data == UPDATE_CLOSE)
async def on_update_close(callback: CallbackQuery, bot: Bot, user: UserDto) -> None:
    """Close update notification."""
    notification: Message = cast(Message, callback.message)
    logger.info(f"{log(user)} Closed update notification '{notification.message_id}'")
    try:
        await notification.delete()
        await callback.answer()
    except Exception:
        try:
            await bot.edit_message_reply_markup(
                chat_id=notification.chat.id,
                message_id=notification.message_id,
                reply_markup=None,
            )
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data.startswith(UPDATE_SNOOZE_PREFIX))
@inject
async def on_update_snooze(
    callback: CallbackQuery,
    bot: Bot,
    user: UserDto,
    update_checker_service: FromDishka[UpdateCheckerService],
) -> None:
    """Handle update notification snooze/dismiss buttons."""
    notification: Message = cast(Message, callback.message)
    action = callback.data.split(":", 1)[1] if callback.data else ""

    try:
        if action == "off":
            await update_checker_service.disable_notifications()
            await callback.answer("🔕", show_alert=False)
            logger.info(f"{log(user)} Disabled update notifications")
        elif action in ("1", "3", "7"):
            days = int(action)
            await update_checker_service.set_snooze(days)
            await callback.answer(f"⏰ {days}d", show_alert=False)
            logger.info(f"{log(user)} Snoozed update notifications for {days} day(s)")
        else:
            await callback.answer()
            return

        # Delete the notification message
        try:
            await notification.delete()
        except Exception:
            try:
                await bot.edit_message_reply_markup(
                    chat_id=notification.chat.id,
                    message_id=notification.message_id,
                    reply_markup=None,
                )
            except Exception:
                pass

    except Exception as e:
        logger.error(f"Failed to handle update snooze: {e}")
        await callback.answer()


@router.callback_query(F.data == "donate_close")
async def on_donate_close(callback: CallbackQuery, bot: Bot) -> None:
    """Close donation notification."""
    notification: Message = cast(Message, callback.message)
    try:
        await notification.delete()
        await callback.answer()
    except Exception:
        try:
            await bot.edit_message_reply_markup(
                chat_id=notification.chat.id,
                message_id=notification.message_id,
                reply_markup=None,
            )
            await callback.answer()
        except Exception:
            pass


@router.callback_query(F.data == "delete_message")
async def on_delete_message(callback: CallbackQuery, bot: Bot) -> None:
    """Удаление сообщения с файлом по кнопке Закрыть"""
    message: Message = cast(Message, callback.message)
    
    try:
        # Удаляем сконвертированный файл
        import os
        sqlite_path = "/opt/dfc-tg/backups/db/sql_convert.db"
        if os.path.exists(sqlite_path):
            os.remove(sqlite_path)
            logger.debug(f"Deleted converted file: {sqlite_path}")
        
        await message.delete()
        try:
            await callback.answer()
        except TelegramBadRequest as e:
            # Query timeout - user clicked button too late, just ignore
            logger.debug(f"Callback query timeout, ignoring: {e}")
    except Exception as exception:
        logger.error(f"Failed to delete message. Exception: {exception}")
