"""
Connection keepalive background task.

Periodically pings PostgreSQL, Redis, and Telegram Bot API to prevent
connection pool entries from going stale during idle periods.

Without this, the first request after extended inactivity suffers from:
  - Stale DB connections being recycled (pool_pre_ping SELECT 1 + reconnect)
  - Redis TCP connections timing out and reconnecting
  - aiohttp sessions to api.telegram.org dropping (TCP + TLS re-handshake)

Running lightweight pings every 30s keeps all connections warm and ensures
instant response times regardless of idle duration.
"""

import asyncio
from typing import Sequence

from aiogram import Bot
from loguru import logger
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


async def keepalive_loop(
    engine: AsyncEngine,
    redis_client: Redis,
    bots: Sequence[Bot],
    *,
    db_redis_interval: int = 30,
    telegram_interval: int = 120,
) -> None:
    """
    Background loop that keeps infrastructure connections warm.

    Args:
        engine: SQLAlchemy async engine for DB pool keepalive.
        redis_client: Redis client for connection keepalive.
        bots: All bot instances (main + mirrors) for Telegram API keepalive.
        db_redis_interval: Seconds between DB/Redis pings (default: 30).
        telegram_interval: Seconds between Telegram API pings (default: 120).
    """
    telegram_counter = 0

    while True:
        await asyncio.sleep(db_redis_interval)
        telegram_counter += db_redis_interval

        # ── Redis ping ──────────────────────────────────────────────────
        try:
            await redis_client.ping()
        except Exception as e:
            logger.warning(f"Keepalive: Redis ping failed: {e}")

        # ── DB ping ─────────────────────────────────────────────────────
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as e:
            logger.warning(f"Keepalive: DB ping failed: {e}")

        # ── Telegram API ping (less frequent) ──────────────────────────
        if telegram_counter >= telegram_interval:
            telegram_counter = 0
            for bot in bots:
                try:
                    await bot.get_me()
                except Exception as e:
                    logger.warning(f"Keepalive: Telegram API ping failed for bot {bot.id}: {e}")
