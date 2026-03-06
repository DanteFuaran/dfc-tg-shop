from abc import ABC

from fluentogram import TranslatorHub
from redis.asyncio import Redis

from src.core.config import AppConfig
from src.infrastructure.redis import RedisRepository


class BaseService(ABC):
    config: AppConfig
    redis_client: Redis
    redis_repository: RedisRepository
    translator_hub: TranslatorHub

    def __init__(
        self,
        config: AppConfig,
        redis_client: Redis,
        redis_repository: RedisRepository,
        translator_hub: TranslatorHub,
    ) -> None:
        self.config = config
        self.redis_client = redis_client
        self.redis_repository = redis_repository
        self.translator_hub = translator_hub
