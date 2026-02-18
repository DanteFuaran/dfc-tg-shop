import inspect
import logging
import sys
from pathlib import Path
from typing import Final
from zipfile import ZipFile

from loguru import logger

from src.core.constants import LOG_DIR

LOG_FILENAME: Final[str] = "bot.log"
LOG_LEVEL: Final[str] = "INFO"  # Change to "DEBUG" for verbose logging
LOG_COMPRESSION: Final[str] = "zip"
LOG_RETENTION: Final[str] = "14 days"
LOG_ENCODING: Final[str] = "utf-8"
LOG_FORMAT: Final[str] = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def compress_log_file(filepath: str) -> None:
    log_file = Path(filepath)
    filename_stem = log_file.stem
    suffix_candidate = filename_stem.rpartition("_")[-1]

    # Remove trailing digit suffix if present (e.g. "_12345")
    if suffix_candidate.isdigit():
        filename_stem = filename_stem[: -(len(suffix_candidate) + 1)]

    original_extension = log_file.suffix
    archive_filename = f"{filename_stem}{original_extension}.{LOG_COMPRESSION}"
    archive_path = log_file.with_name(archive_filename)

    with ZipFile(archive_path, "w") as archive:
        archive.write(log_file, arcname=LOG_FILENAME)

    log_file.unlink()


def setup_logger(rotation: bool = True) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()

    logger.add(
        sink=sys.stderr,
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        colorize=True,
    )

    if rotation:
        # Main process: writes to file with rotation by size, retention and compression
        logger.add(
            sink=LOG_DIR / LOG_FILENAME,
            level=LOG_LEVEL,
            format=LOG_FORMAT,
            rotation="50 MB",
            retention=LOG_RETENTION,
            compression=compress_log_file,
            encoding=LOG_ENCODING,
        )
    else:
        # Worker/scheduler: append to the same file, no rotation
        logger.add(
            sink=LOG_DIR / LOG_FILENAME,
            level=LOG_LEVEL,
            format=LOG_FORMAT,
            rotation=None,
            encoding=LOG_ENCODING,
        )

    intercept_handler = InterceptHandler()
    logging.basicConfig(handlers=[intercept_handler], level=logging.INFO, force=True)

    # Настройка уровней логирования для внешних библиотек
    for logger_name in (
        "uvicorn",
        "uvicorn.error",
        "fastapi",
    ):
        ext_logger = logging.getLogger(logger_name)
        ext_logger.handlers = [intercept_handler]
        ext_logger.propagate = False  # Предотвращаем дублирование логов

    # Отключаем uvicorn.access логи (HTTP запросы) - слишком много
    logging.getLogger("uvicorn.access").disabled = True
    
    # Уменьшаем verbose логирование aiogram
    logging.getLogger("aiogram.dispatcher").setLevel(logging.WARNING)
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    logging.getLogger("aiogram.middlewares").setLevel(logging.WARNING)
    
    # Отключаем/уменьшаем логирование SQLAlchemy
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    
    # Уменьшаем логирование для Redis
    logging.getLogger("redis").setLevel(logging.WARNING)
    
    # logging.getLogger("httpx").propagate = False
    logging.getLogger("httpx").setLevel(logging.WARNING)
