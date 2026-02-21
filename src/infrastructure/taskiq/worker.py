import asyncio
from typing import Any

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from taskiq import TaskiqMiddleware
from taskiq_redis import RedisStreamBroker
from loguru import logger

from src.bot.dispatcher import create_bg_manager_factory, create_dispatcher
from src.core.config import AppConfig
from src.core.logger import setup_logger
from src.infrastructure.di import create_container
from src.infrastructure.taskiq.init import init as init_consumer_group
from src.services.mirror_bot import MirrorBotService
from src.services.notification import NotificationService

from .broker import broker


class SimpleMirrorBotManager:
    """Lightweight wrapper that holds mirror bot instances for notification sending."""
    def __init__(self) -> None:
        self._bots: dict[int, Bot] = {}

    @property
    def active_bots(self) -> dict[int, Bot]:
        return dict(self._bots)

    def add_bot(self, bot_id: int, bot: Bot) -> None:
        self._bots[bot_id] = bot

    async def close_all(self) -> None:
        for bot in self._bots.values():
            try:
                await bot.session.close()
            except Exception:
                pass


class DishkaParamsFilterMiddleware(TaskiqMiddleware):
    """Middleware для фильтрации параметров dishka из task_hints.
    
    Это необходимо потому что dishka добавляет параметр dishka_container в сигнатуру,
    но taskiq пытается его десериализовать через Pydantic, что приводит к ошибке.
    Dishka middleware сам обработает инжекцию зависимостей.
    """
    
    def __init__(self, container: Any) -> None:
        self.container = container
        self._mirror_initialized = False
    
    async def startup(self) -> None:
        """При старте очищаем task_hints от dishka параметров и инициализируем зеркальные боты."""
        if hasattr(self.broker, 'task_hints'):
            # Удаляем dishka_container из hints для всех задач
            filtered_hints: dict[str, dict[str, Any]] = {}
            for task_name, hints in self.broker.task_hints.items():
                filtered_hints[task_name] = {
                    key: value for key, value in hints.items()
                    if key != 'dishka_container'
                }
            self.broker.task_hints = filtered_hints
        
        # Initialize mirror bots for notification broadcasting
        if not self._mirror_initialized:
            await self._initialize_mirror_bots()
            self._mirror_initialized = True
    
    async def _initialize_mirror_bots(self) -> None:
        """Initialize mirror bots from database and register with NotificationService."""
        logger.info("Initializing mirror bots for notifications...")
        try:
            async with self.container(scope="taskiq") as task_container:
                mirror_bot_service: MirrorBotService = await task_container.get(MirrorBotService)
                active_mirrors = await mirror_bot_service.get_active()
                logger.info(f"Found {len(active_mirrors)} active mirror bots")

            if active_mirrors:
                mirror_manager = SimpleMirrorBotManager()
                for mirror_bot_dto in active_mirrors:
                    try:
                        mirror_bot_instance = Bot(
                            token=mirror_bot_dto.token,
                            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
                        )
                        mirror_manager.add_bot(mirror_bot_dto.id, mirror_bot_instance)
                        logger.debug(f"Mirror bot {mirror_bot_dto.id} initialized")
                    except Exception as e:
                        logger.warning(f"Failed to initialize mirror bot {mirror_bot_dto.id}: {e}")

                NotificationService.set_mirror_bot_manager(mirror_manager)
                logger.info(f"✓ Mirror bot manager set ({len(mirror_manager.active_bots)} bots)")
            else:
                logger.info("No active mirror bots found")
        except Exception as e:
            logger.warning(f"Failed to initialize mirror bots: {e}")


def worker() -> RedisStreamBroker:
    setup_logger(rotation=False)

    # Initialize consumer group before starting workers
    init_consumer_group()

    config = AppConfig.get()

    # Worker не обрабатывает Telegram-апдейты — ему не нужны хэндлеры, middleware, фильтры.
    # Загружаем только Dispatcher (для FSM storage) и BgManagerFactory (для redirect-задач).
    # setup_dispatcher() НЕ вызываем — это экономит ~30-50 МБ RAM на каждом процессе,
    # т.к. не загружаются все модули роутеров, хэндлеров и middleware.
    dispatcher = create_dispatcher(config=config)
    bg_manager_factory = create_bg_manager_factory(dispatcher=dispatcher)

    container = create_container(config=config, bg_manager_factory=bg_manager_factory)

    setup_taskiq_dishka(container=container, broker=broker)
    
    # Добавляем middleware для фильтрации dishka параметров из task_hints и инициализации зеркальных ботов
    broker.add_middlewares(DishkaParamsFilterMiddleware(container=container))

    return broker
