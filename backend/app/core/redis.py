import random
from typing import Any

from loguru import logger
from pydantic_core import from_json, to_json
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import settings

redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def set_cache(cache_key: str, data: Any, ttl: int | None = None) -> None:

    try:
        ttl = ttl or settings.CACHE_TTL + random.randint(0, 90)
        to_cache_data = to_json(data)

        await redis_client.set(name=cache_key, value=to_cache_data, ex=ttl)
    except Exception as e:
        logger.opt(exception=True, depth=1).error(
            "Redis cache write failed: err={} cache_key={} ttl={}",
            type(e).__name__,
            cache_key,
            ttl,
        )


async def get_cache(cache_key: str) -> None:
    try:
        if cache_key is not None:
            cached_data = await redis_client.get(name=cache_key)
            if cached_data is not None:
                logger.debug(
                    "Redis Cache HIT: Returning cached data for cache key: {}",
                    cache_key,
                )
                return from_json(cached_data)
        return None
    except Exception as e:
        logger.opt(exception=True, depth=1).error(
            "Redis Cache MISS: err={} cache_key={}",
            type(e).__name__,
            cache_key,
        )
    return None


async def delete_cache(*cache_keys: str):
    try:
        await redis_client.unlink(*cache_keys)
    except Exception as e:
        logger.opt(exception=True, depth=1).error(
            "Redis cache unlinking failed: err={} cache_key={}",
            type(e).__name__,
            cache_keys,
        )
