import redis
from config.settings import settings
import json


class RedisStore:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def set_cache(self, key: str, value, ttl: int = None):
        if isinstance(value, dict):
            value = json.dumps(value)
        if ttl is None:
            ttl = settings.REDIS_CACHE_TTL
        self.client.set(key, value, ex=ttl)

    def get_cache(self, key: str):
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    def delete_cache(self, key: str):
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0

    def get_keys(self, pattern: str = "*") -> list:
        return self.client.keys(pattern)

    def flush_db(self):
        self.client.flushdb()