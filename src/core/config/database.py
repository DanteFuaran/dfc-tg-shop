from pydantic import PostgresDsn, SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from .base import BaseConfig
from .validators import validate_not_change_me


class DatabaseConfig(BaseConfig, env_prefix="DATABASE_"):
    host: str = "dfc-tg-db"
    port: int = 5432
    name: str = "dfc-tg"
    user: str = "dfc-tg"
    password: SecretStr

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 15  # Достаточно для 3 контейнеров (bot, worker, scheduler)
    max_overflow: int = 25  # Запас при пиковой нагрузке
    pool_timeout: int = 30  # Увеличено для стабильности при высокой нагрузке
    pool_recycle: int = 1800  # Переиспользование соединений каждые 30 минут
    pool_pre_ping: bool = True  # Проверка соединения перед использованием

    @property
    def dsn(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.name,
        ).unicode_string()

    @field_validator("password")
    @classmethod
    def validate_database_password(cls, field: SecretStr, info: FieldValidationInfo) -> SecretStr:
        validate_not_change_me(field, info)
        return field
