import asyncio
import traceback
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional

from aiogram import Bot, Dispatcher
from aiogram.types import WebhookInfo, User as AiogramUser, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.formatting import Text
from dishka import AsyncContainer, Scope
from fastapi import FastAPI
from fluentogram import TranslatorHub
from loguru import logger
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.__version__ import __version__
from src.api.endpoints import TelegramWebhookEndpoint
from src.core.config.app import AppConfig
from src.core.enums import SystemNotificationType, UserRole
from src.core.storage.keys import ShutdownMessagesKey, UpdateInProgressKey, UpdateMessageKey
from src.core.utils.message_payload import MessagePayload
from src.infrastructure.database import UnitOfWork
from src.infrastructure.redis.repository import RedisRepository
from src.core.keepalive import keepalive_loop
from src.services.command import CommandService
from src.services.mirror_bot import MirrorBotService
from src.services.mirror_bot_manager import MirrorBotManager
from src.services.notification import NotificationService
from src.services.payment_gateway import PaymentGatewayService
from src.services.remnawave import RemnawaveService
from src.services.settings import SettingsService
from src.services.user import UserService
from src.services.webhook import WebhookService


async def send_shutdown_notifications(container: AsyncContainer) -> None:
    """Send shutdown notifications to all DEV users."""
    logger.info("Shutdown: sending shutdown notifications...")
    
    try:
        async with container(scope=Scope.REQUEST) as shutdown_container:
            notification_service: NotificationService = await shutdown_container.get(NotificationService)
            redis_repository: RedisRepository = await shutdown_container.get(RedisRepository)
            user_service: UserService = await shutdown_container.get(UserService)
            settings_service: SettingsService = await shutdown_container.get(SettingsService)

            # Skip shutdown notification if shutdown is caused by an update
            update_in_progress = await redis_repository.get(UpdateInProgressKey(), str)
            logger.info(f"Shutdown: UpdateInProgressKey = {update_in_progress}")
            if update_in_progress:
                logger.info("Shutdown caused by update — skipping shutdown notification")
                return

            devs = await user_service.get_by_role(role=UserRole.DEV)
            settings = await settings_service.get()
            
            logger.info(f"Shutdown: found {len(devs) if devs else 0} DEV users")

            shutdown_key = ShutdownMessagesKey()

            for dev in devs:
                try:
                    if settings.features.language_enabled:
                        locale = dev.language
                    else:
                        locale = settings.bot_locale

                    logger.info(f"Shutdown: sending notification to DEV user {dev.telegram_id} (locale: {locale})")
                    mirror_sent_out: list[tuple[int, Any]] = []
                    msg = await notification_service._send_message(
                        user=dev,
                        payload=MessagePayload.not_deleted(
                            i18n_key="ntf-event-bot-shutdown",
                            add_close_button=False,
                        ),
                        locale_override=locale,
                        mirror_sent_out=mirror_sent_out,
                    )
                    if msg:
                        # Format: "main:{chat_id}:{msg_id}" for main bot
                        await redis_repository.list_push(shutdown_key, f"main:{dev.telegram_id}:{msg.message_id}")
                        logger.info(f"Shutdown: sent message {msg.message_id} for chat {dev.telegram_id}")
                    else:
                        logger.warning(f"Shutdown: _send_message returned None for {dev.telegram_id}")
                    # Store mirror bot message IDs for cleanup on startup
                    # Format: "{mirror_db_id}:{chat_id}:{msg_id}"
                    for mirror_db_id, mirror_msg in mirror_sent_out:
                        await redis_repository.list_push(
                            shutdown_key,
                            f"{mirror_db_id}:{dev.telegram_id}:{mirror_msg.message_id}",
                        )
                        logger.debug(f"Shutdown: stored mirror[{mirror_db_id}] message {mirror_msg.message_id}")
                except Exception as e:
                    logger.error(f"Shutdown: Failed to send notification to {dev.telegram_id}: {e}", exc_info=True)

            await redis_repository.expire(shutdown_key, 86400)
            logger.info("Shutdown: notifications sent successfully")
    except Exception as e:
        logger.error(f"Shutdown: Failed to send notifications: {e}", exc_info=True)


async def ensure_dev_user_exists(
    config: AppConfig,
    bot: Bot,
    max_retries: int = 5,
    retry_delay: float = 2.0,
) -> bool:
    """
    Create DEV user if not exists using a separate database connection.
    Uses retry logic to handle transient database issues during startup.
    Returns True if user exists or was created, False otherwise.
    """
    dev_telegram_id = config.bot.dev_id
    
    for attempt in range(1, max_retries + 1):
        engine = None
        try:
            # Create a separate lightweight connection for this operation
            engine = create_async_engine(
                url=config.database.dsn,
                pool_size=1,
                max_overflow=0,
                pool_timeout=5,
                pool_pre_ping=True,
                connect_args={
                    "timeout": 10,
                    "command_timeout": 15,
                },
            )
            
            async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
            
            async with UnitOfWork(async_session) as uow:
                # Check if DEV user exists
                existing_user = await uow.repository.users.get(dev_telegram_id)
                
                if existing_user:
                    logger.debug(f"DEV user {dev_telegram_id} already exists")
                    return True
                
                # Get Telegram user info
                try:
                    dev_chat = await bot.get_chat(dev_telegram_id)
                except Exception as e:
                    logger.warning(f"Failed to get Telegram info for DEV user {dev_telegram_id}: {e}")
                    return False
                
                # Create AiogramUser object
                aiogram_user = AiogramUser(
                    id=dev_telegram_id,
                    is_bot=False,
                    first_name=dev_chat.first_name or "DEV",
                    last_name=dev_chat.last_name,
                    username=dev_chat.username,
                    language_code=config.default_locale.value,
                )
                
                # Create user using service logic
                from src.core.utils.generators import generate_referral_code
                from src.infrastructure.database.models.sql import User
                from src.infrastructure.database.models.dto import UserDto
                
                user_dto = UserDto(
                    telegram_id=aiogram_user.id,
                    username=aiogram_user.username,
                    referral_code=generate_referral_code(
                        aiogram_user.id,
                        secret=config.crypt_key.get_secret_value(),
                    ),
                    name=aiogram_user.full_name,
                    role=UserRole.DEV,
                    language=config.default_locale,
                )
                
                db_user = User(**user_dto.model_dump())
                await uow.repository.users.create(db_user)
                await uow.commit()
                
                logger.success(f"DEV user {dev_telegram_id} created automatically on first startup")
                return True
                
        except Exception as e:
            logger.warning(f"Attempt {attempt}/{max_retries} to create DEV user failed: {e}")
            if attempt < max_retries:
                await asyncio.sleep(retry_delay * attempt)  # Exponential backoff
        finally:
            if engine:
                await engine.dispose()
    
    logger.error(f"Failed to create DEV user after {max_retries} attempts")
    return False


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    dispatcher: Dispatcher = app.state.dispatcher
    telegram_webhook_endpoint: TelegramWebhookEndpoint = app.state.telegram_webhook_endpoint
    container: AsyncContainer = app.state.dishka_container

    update_completed = False

    async with container(scope=Scope.REQUEST) as startup_container:
        config: AppConfig = await startup_container.get(AppConfig)
        webhook_service: WebhookService = await startup_container.get(WebhookService)
        command_service: CommandService = await startup_container.get(CommandService)
        settings_service: SettingsService = await startup_container.get(SettingsService)
        gateway_service: PaymentGatewayService = await startup_container.get(PaymentGatewayService)
        remnawave_service: RemnawaveService = await startup_container.get(RemnawaveService)
        notification_service: NotificationService = await startup_container.get(NotificationService)
        redis_repository: RedisRepository = await startup_container.get(RedisRepository)
        user_service: UserService = await startup_container.get(UserService)
        bot: Bot = await startup_container.get(Bot)

        await gateway_service.create_default()
        settings = await settings_service.get()
        
        # Check if this startup is after an update (UpdateInProgressKey is only set during updates, not restarts)
        try:
            update_in_progress_key = UpdateInProgressKey()
            update_flag = await redis_repository.get(update_in_progress_key, str)
            if update_flag:
                update_completed = True
                await redis_repository.delete(update_in_progress_key)
                logger.info("Detected post-update startup")
        except Exception as e:
            logger.warning(f"Failed to check update flag: {e}")

        # NOTE: Shutdown/update messages are NOT deleted here.
        # They stay visible until the bot is fully started (after yield).
        # Deletion happens in _send_startup_notifications() right before
        # sending the main menu, so the user always sees either
        # "Bot stopped" or "Updating..." until the bot is ready.
        
        # Initialize Redis consumer group for taskiq
        try:
            redis = await from_url(config.redis.dsn)
            await redis.xgroup_create(name="taskiq", groupname="taskiq", id="0", mkstream=True)
            await redis.close()
        except Exception as exc:
            # Consumer group might already exist, which is fine
            if "BUSYGROUP" not in str(exc):
                logger.warning(f"Failed to initialize consumer group: {exc}")

    await startup_container.close()

    allowed_updates = dispatcher.resolve_used_update_types()
    webhook_info: WebhookInfo = await webhook_service.setup(allowed_updates)

    if webhook_service.has_error(webhook_info):
        logger.critical(f"Webhook has a last error message: '{webhook_info.last_error_message}'")
        await notification_service.system_notify(
            ntf_type=SystemNotificationType.BOT_LIFETIME,
            payload=MessagePayload.not_deleted(
                i18n_key="ntf-event-error-webhook",
                i18n_kwargs={"error": webhook_info.last_error_message},
            ),
        )

    await command_service.setup()
    await telegram_webhook_endpoint.startup()

    # ── Start mirror (additional) bots ──────────────────────────────────
    mirror_bot_manager: MirrorBotManager = app.state.mirror_bot_manager
    try:
        async with container(scope=Scope.REQUEST) as mirror_container:
            mirror_service: MirrorBotService = await mirror_container.get(MirrorBotService)
            active_mirrors = await mirror_service.get_active()

        if active_mirrors:
            logger.info(f"Starting {len(active_mirrors)} mirror bot(s)...")
            for mirror in active_mirrors:
                started = await mirror_bot_manager.start_mirror_bot(mirror, allowed_updates)
                if not started:
                    logger.warning(f"Failed to start mirror bot @{mirror.username} (id={mirror.id})")
            logger.info(f"Mirror bots running: {len(mirror_bot_manager.active_bots)}")

            # Set up bot commands for each mirror bot (same as main bot)
            for mirror_db_id, mirror_bot in mirror_bot_manager.active_bots.items():
                try:
                    await command_service.setup_for_bot(mirror_bot)
                except Exception as e:
                    logger.warning(f"Failed to set commands for mirror bot {mirror_db_id}: {e}")
        else:
            logger.debug("No active mirror bots to start")
    except Exception as e:
        logger.warning(f"Failed to start mirror bots: {e}")

    # Register mirror bot manager in NotificationService so all notifications
    # are automatically forwarded to mirror bots as well.
    from src.services.notification import NotificationService as _NtfSvc
    _NtfSvc.set_mirror_bot_manager(mirror_bot_manager)

    bot: Bot = await container.get(Bot)
    bot_info = await bot.get_me()
    states: dict[Optional[bool], str] = {True: "Enabled", False: "Disabled", None: "Unknown"}

    logger.opt(colors=True).info(
        rf"""
        
    <cyan>██████╗   ███████╗  ██████╗</>
    <cyan>██╔══██╗  ██╔════╝ ██╔════╝</>
    <cyan>██║  ██║  █████╗   ██║     </>
    <cyan>██║  ██║  ██╔══╝   ██║     </>
    <cyan>██████╔╝  ██║      ╚██████╗</>
    <cyan>╚═════╝   ╚═╝       ╚═════╝</>
    <cyan> Digital  Freedom   Core</>

        <green>Version: {__version__}</>
        <cyan>------------------------</>
        Groups Mode  - {states[bot_info.can_join_groups]}
        Privacy Mode - {states[not bot_info.can_read_all_group_messages]}
        Inline Mode  - {states[bot_info.supports_inline_queries]}
        <cyan>------------------------</>
        <yellow>Bot in access mode: '{settings.access_mode}'</>
        <yellow>Purchases allowed: '{settings.purchases_allowed}'</>
        <yellow>Registration allowed: '{settings.registration_allowed}'</>
        """  # noqa: W605
    )
    await asyncio.sleep(2)

    # ── Prepare data for startup notifications ──────────────────────────
    # Do all DB/cache work BEFORE sending any messages to avoid timing issues
    startup_devs = None
    startup_settings_ok = False
    startup_i18n_data = {}
    try:
        from src.core.i18n.translator import get_translated_kwargs
        from src.core.utils.formatters import i18n_postprocess_text
        from fluentogram import TranslatorHub
        from src.bot.states import Notification

        translator_hub: TranslatorHub = await container.get(TranslatorHub)

        # Ensure DEV user exists (creates if not)
        dev_user_created = await ensure_dev_user_exists(config, bot)

        # Clear user cache if we just created DEV user
        if dev_user_created:
            try:
                await redis_repository.delete_pattern("cache:get_by_role:*")
                await redis_repository.delete_pattern("cache:get_user:*")
            except Exception as e:
                logger.debug(f"Failed to clear cache after DEV user creation: {e}")

        # DB-запросы через отдельный scope, т.к. startup_container уже закрыт
        # и его UoW.session = None (commit будет no-op)
        async with container(scope=Scope.REQUEST) as prep_container:
            prep_user_svc: UserService = await prep_container.get(UserService)
            prep_settings_svc: SettingsService = await prep_container.get(SettingsService)
            startup_devs = await prep_user_svc.get_by_role(role=UserRole.DEV)
            startup_settings_ok = await prep_settings_svc.is_notification_enabled(SystemNotificationType.BOT_LIFETIME)

        if not startup_devs:
            logger.warning(f"DEV user creation failed. Please send /start to the bot from Telegram ID: {config.bot.dev_id}")

        # Pre-render i18n texts per user
        if startup_devs and startup_settings_ok:
            for dev in startup_devs:
                try:
                    locale = dev.language if settings.features.language_enabled else settings.bot_locale
                    i18n = translator_hub.get_translator_by_locale(locale=locale)
                    kwargs = get_translated_kwargs(i18n, {
                        "mode": settings.access_mode,
                        "purchases_allowed": settings.purchases_allowed,
                        "registration_allowed": settings.registration_allowed,
                    })
                    text = i18n_postprocess_text(i18n.get("ntf-event-bot-startup", **kwargs))
                    close_btn_text = i18n.get("btn-notification-close-success")
                    startup_i18n_data[dev.telegram_id] = (text, close_btn_text)
                except Exception as e:
                    logger.warning(f"Failed to prepare startup text for {dev.telegram_id}: {e}")
    except Exception as e:
        logger.warning(f"Failed to prepare startup notification data: {e}")

    # ── 0. Remnawave connection & DEV user subscription sync ───────────
    # Выполняем ДО показа главного меню, чтобы DEV-пользователь видел подписку.
    # ВАЖНО: используем отдельный DI-scope с ЖИВЫМ UoW/сессией.
    # startup_container уже закрыт → его UoW.session = None → commit() = no-op
    # → INSERT/UPDATE отправляются через flush(), но НИКОГДА не коммитятся
    # → при завершении сессии транзакция откатывается → данные теряются.
    try:
        async with container(scope=Scope.REQUEST) as sync_container:
            sync_remnawave: RemnawaveService = await sync_container.get(RemnawaveService)
            sync_user_svc: UserService = await sync_container.get(UserService)
            sync_redis: RedisRepository = await sync_container.get(RedisRepository)

            await sync_remnawave.try_connection()

            # Синхронизация DEV-пользователя: он создаётся в ensure_dev_user_exists
            # напрямую в БД без проверки Remnawave, поэтому при первом запуске
            # у него может не быть подписки. Проверяем и синхронизируем.
            try:
                dev_user = await sync_user_svc.get_without_cache(telegram_id=config.bot.dev_id)
                if dev_user and not dev_user.current_subscription:
                    existing_remna_users = await sync_remnawave.remnawave.users.get_users_by_telegram_id(
                        telegram_id=str(config.bot.dev_id)
                    )
                    if existing_remna_users:
                        await sync_remnawave.sync_user(existing_remna_users[0], creating=False)
                        # Очищаем ВСЕ кеши чтобы главное меню увидело подписку
                        await sync_user_svc.clear_user_cache(config.bot.dev_id)
                        await sync_redis.delete_pattern("cache:get_user:*")
                        await sync_redis.delete_pattern("cache:get_by_role:*")
                        await sync_redis.delete_pattern("cache:get_subscription:*")
                        await sync_redis.delete_pattern("cache:get_current_subscription:*")
                        logger.info(f"Synced DEV user {config.bot.dev_id} subscription from Remnawave")
                    else:
                        logger.debug(f"DEV user {config.bot.dev_id} not found in Remnawave, skipping sync")
            except Exception as e:
                logger.warning(f"Failed to sync DEV user subscription from Remnawave: {e}")

    except Exception as exception:
        logger.exception(f"Remnawave connection failed: {exception}")
        error_type_name = type(exception).__name__
        error_message = Text(str(exception)[:512])

        try:
            await notification_service.error_notify(
                traceback_str=traceback.format_exc(),
                payload=MessagePayload.not_deleted(
                    i18n_key="ntf-event-error-remnawave",
                    i18n_kwargs={
                        "error": f"{error_type_name}: {error_message.as_html()}",
                    },
                ),
            )
        except Exception:
            logger.warning("Failed to send Remnawave error notification")

    # ── Startup notifications (deferred until after server is ready) ──
    # All notifications are sent AFTER yield (Application startup complete)
    # so that the user can interact with menus immediately.
    async def _send_startup_notifications() -> None:
        """Send all startup notifications after the server starts accepting webhooks."""

        async def _send_all(chat_id: int, **kwargs) -> None:
            """Send a message via main bot and all active mirror bots."""
            for _b in [bot] + list(mirror_bot_manager.active_bots.values()):
                try:
                    await _b.send_message(chat_id=chat_id, **kwargs)
                except Exception as _e:
                    logger.debug(f"Bot {_b.id} failed to send startup message to {chat_id}: {_e}")

        await asyncio.sleep(2)  # Wait for uvicorn to fully start accepting requests
        logger.debug("Sending deferred startup notifications...")

        # ── 0. Delete previous shutdown/update messages ─────────────────
        # These messages stayed visible until now to indicate the bot is not ready.
        # Now that the server is accepting webhooks, we can safely remove them.
        try:
            async with container(scope=Scope.REQUEST) as cleanup_container:
                cleanup_redis: RedisRepository = await cleanup_container.get(RedisRepository)

                # Delete shutdown messages ("Bot stopped" notifications)
                try:
                    shutdown_key = ShutdownMessagesKey()
                    shutdown_messages = await cleanup_redis.list_range(shutdown_key, 0, -1)
                    for msg_data in shutdown_messages:
                        try:
                            parts = msg_data.split(":")
                            if len(parts) == 3:
                                bot_key, chat_id_str, msg_id_str = parts
                                chat_id = int(chat_id_str)
                                message_id = int(msg_id_str)
                                if bot_key == "main":
                                    delete_bot = bot
                                else:
                                    # Look up mirror bot by DB id
                                    db_id = int(bot_key)
                                    delete_bot = mirror_bot_manager.active_bots.get(db_id)
                                    if not delete_bot:
                                        logger.debug(f"Mirror bot {db_id} not active, skipping deletion of msg {message_id}")
                                        continue
                            elif len(parts) == 2:
                                # Legacy format: "{chat_id}:{msg_id}" — use main bot
                                chat_id = int(parts[0])
                                message_id = int(parts[1])
                                delete_bot = bot
                            else:
                                logger.warning(f"Unknown shutdown message format: {msg_data}")
                                continue
                            await delete_bot.delete_message(chat_id=chat_id, message_id=message_id)
                            logger.debug(f"Deleted shutdown message {message_id} in chat {chat_id}")
                        except Exception as e:
                            logger.warning(f"Failed to delete shutdown message '{msg_data}': {e}")
                    await cleanup_redis.delete(shutdown_key)
                except Exception as e:
                    logger.warning(f"Failed to cleanup shutdown messages: {e}")

                # Delete update message ("Updating..." notification)
                try:
                    update_msg_key = UpdateMessageKey()
                    update_msg_data = await cleanup_redis.get(update_msg_key, str)
                    if update_msg_data:
                        chat_id, message_id = update_msg_data.split(":")
                        try:
                            await bot.delete_message(chat_id=int(chat_id), message_id=int(message_id))
                            logger.debug(f"Deleted update message {message_id} in chat {chat_id}")
                        except Exception as e:
                            logger.warning(f"Failed to delete update message: {e}")
                        await cleanup_redis.delete(update_msg_key)
                except Exception as e:
                    logger.warning(f"Failed to cleanup update message: {e}")
        except Exception as e:
            logger.warning(f"Failed to cleanup startup messages: {e}")

        # ── 1. Main menu (FIRST — will appear at the TOP) ──────────────
        try:
            from aiogram_dialog import BgManagerFactory, StartMode, ShowMode
            from src.bot.states import MainMenu

            dev_id = config.bot.dev_id
            bg_manager_factory: BgManagerFactory = await container.get(BgManagerFactory)
            bg_manager = bg_manager_factory.bg(
                bot=bot,
                user_id=dev_id,
                chat_id=dev_id,
            )
            await bg_manager.start(
                state=MainMenu.MAIN,
                mode=StartMode.RESET_STACK,
                show_mode=ShowMode.DELETE_AND_SEND,
            )
            await asyncio.sleep(3)  # Wait for aiogram-dialog to fully render
            logger.info(f"Redirected DEV user {dev_id} to main menu on startup")
        except Exception as e:
            logger.warning(f"Failed to redirect DEV user to main menu: {e}")

        # ── 2. Donation notification (SECOND — middle) ─────────────────
        try:
            devs_for_donate = startup_devs
            if devs_for_donate:
                donate_text = (
                    "💝 <b>Поддержать проект</b>\n\n"
                    "Вы можете поддержать разработку проекта финансово.\n"
                    "Это помогает выпускать обновления чаще и добавлять новые возможности.\n\n"
                    "🔹 <b>ЮMoney:</b>\n<code>4100118836481809</code>\n\n"
                    "🔹 <b>USDT (TRC-20):</b>\n<code>THqJQsgbWY7Tw1BxdLA6SQAkBGVmMhzeLZ</code>\n\n"
                    "🔹 <b>BTC (BEP-20):</b>\n<code>0x657685922d7a9c50e3e90cae3ba9905985349fbb</code>\n\n"
                    "<i>Благодарю за доверие и участие! 💪</i>"
                )
                donate_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="⭐ GitHub", url="https://github.com/DanteFuaran/dfc-tg-shop", style="primary"),
                        InlineKeyboardButton(text="💬 Telegram", url="https://t.me/dfc_soft", style="primary")
                    ],
                    [InlineKeyboardButton(text="✅ Закрыть", callback_data="donate_close", style="success")]
                ])
                for dev in devs_for_donate:
                    try:
                        await _send_all(
                            dev.telegram_id,
                            text=donate_text,
                            reply_markup=donate_keyboard,
                            disable_web_page_preview=True,
                        )
                    except Exception as e:
                        logger.warning(f"Failed to send donation notification to {dev.telegram_id}: {e}")
        except Exception as e:
            logger.warning(f"Failed to send donation notification: {e}")

        await asyncio.sleep(0.3)  # Ensure ordering

        # ── 3. Startup status notification (THIRD — bottom) ────────────
        try:
            from src.bot.states import Notification

            if startup_devs and startup_settings_ok:
                for dev in startup_devs:
                    try:
                        data = startup_i18n_data.get(dev.telegram_id)
                        if not data:
                            continue
                        text, close_btn_text = data
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text=close_btn_text, callback_data=Notification.CLOSE.state, style="success")]
                        ])
                        await _send_all(
                            dev.telegram_id,
                            text=text,
                            reply_markup=keyboard,
                        )
                        logger.debug(f"Sent startup notification to {dev.telegram_id}")
                    except Exception as e:
                        logger.warning(f"Failed to send startup notification to {dev.telegram_id}: {e}")
        except Exception as e:
            logger.warning(f"Failed to send startup notification: {e}")

        # Check for updates on startup
        try:
            from src.services.update_checker import UpdateCheckerService
            async with container(scope=Scope.REQUEST) as update_container:
                update_checker: UpdateCheckerService = await update_container.get(UpdateCheckerService)
                await update_checker.check_for_updates()
        except Exception as e:
            logger.warning(f"Failed to check for updates on startup: {e}")

        # Post-update: show success notification (LAST, after all other notifications)
        if update_completed:
            try:
                dev_id = config.bot.dev_id
                success_msg = await bot.send_message(
                    chat_id=dev_id,
                    text="✅ <b>Бот успешно обновлен!</b>",
                    parse_mode="HTML",
                )
                for _mb in mirror_bot_manager.active_bots.values():
                    try:
                        await _mb.send_message(chat_id=dev_id, text="✅ <b>Бот успешно обновлен!</b>", parse_mode="HTML")
                    except Exception:
                        pass

                async def _auto_delete_success() -> None:
                    await asyncio.sleep(5)
                    try:
                        await bot.delete_message(
                            chat_id=dev_id,
                            message_id=success_msg.message_id,
                        )
                    except Exception:
                        pass

                asyncio.create_task(_auto_delete_success())
            except Exception as e:
                logger.warning(f"Failed to send post-update success notification: {e}")

    # Schedule notifications to be sent after server starts
    asyncio.create_task(_send_startup_notifications())

    # ── Start connection keepalive task ─────────────────────────────────
    # Keeps DB pool, Redis connections, and Telegram API aiohttp sessions warm.
    # Without this, the first request after idle suffers reconnection delays.
    try:
        _engine: AsyncEngine = await container.get(AsyncEngine)
        _redis: Redis = await container.get(Redis)
        _all_bots = [bot] + list(mirror_bot_manager.active_bots.values())
        _keepalive_task = asyncio.create_task(
            keepalive_loop(engine=_engine, redis_client=_redis, bots=_all_bots)
        )
        app.state.keepalive_task = _keepalive_task
        logger.info(f"Connection keepalive started ({len(_all_bots)} bot(s))")
    except Exception as e:
        logger.warning(f"Failed to start keepalive task: {e}")

    yield

    # ── Cancel keepalive task ───────────────────────────────────────────
    keepalive_task = getattr(app.state, "keepalive_task", None)
    if keepalive_task and not keepalive_task.done():
        keepalive_task.cancel()
        try:
            await keepalive_task
        except asyncio.CancelledError:
            pass

    # Send shutdown notifications
    logger.info("Lifespan shutdown: starting shutdown notifications")
    await send_shutdown_notifications(container)

    # Stop mirror bots
    try:
        mirror_bot_manager: MirrorBotManager = app.state.mirror_bot_manager
        await mirror_bot_manager.stop_all()
        logger.info("All mirror bots stopped")
    except Exception as e:
        logger.warning(f"Failed to stop mirror bots: {e}")

    await telegram_webhook_endpoint.shutdown()
    await command_service.delete()
    await webhook_service.delete()

    await container.close()
