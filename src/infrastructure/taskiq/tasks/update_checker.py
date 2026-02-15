from dishka.integrations.taskiq import FromDishka, inject
from loguru import logger

from src.infrastructure.taskiq.broker import broker
from src.services.update_checker import UpdateCheckerService


@broker.task(schedule=[{"cron": "0 12 * * *"}])  # Every day at 12:00 UTC
@inject
async def check_bot_update_task(
    update_checker_service: FromDishka[UpdateCheckerService],
) -> None:
    """Scheduled task to check for bot updates once a day."""
    logger.info("[check_bot_update] Starting daily update check")
    await update_checker_service.check_for_updates()
    logger.info("[check_bot_update] Update check completed")
