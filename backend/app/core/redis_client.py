import redis.asyncio as redis
from typing import Optional
import json

from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
    
    async def connect(self):
        self.redis = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    async def disconnect(self):
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)
    
    async def set(self, key: str, value: str, ex: Optional[int] = None):
        await self.redis.set(key, value, ex=ex)
    
    async def delete(self, key: str):
        await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key) > 0
    
    async def expire(self, key: str, seconds: int):
        await self.redis.expire(key, seconds)
    
    async def hget(self, name: str, key: str) -> Optional[str]:
        return await self.redis.hget(name, key)
    
    async def hset(self, name: str, key: str, value: str):
        await self.redis.hset(name, key, value)
    
    async def hgetall(self, name: str) -> dict:
        return await self.redis.hgetall(name)
    
    async def hdel(self, name: str, *keys):
        await self.redis.hdel(name, *keys)
    
    async def publish(self, channel: str, message: dict):
        await self.redis.publish(channel, json.dumps(message))
    
    async def subscribe(self, channel: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        return pubsub
    
    async def lpush(self, key: str, *values):
        await self.redis.lpush(key, *values)
    
    async def lrange(self, key: str, start: int, end: int) -> list:
        return await self.redis.lrange(key, start, end)
    
    async def llen(self, key: str) -> int:
        return await self.redis.llen(key)
    
    async def sadd(self, key: str, *values):
        await self.redis.sadd(key, *values)
    
    async def srem(self, key: str, *values):
        await self.redis.srem(key, *values)
    
    async def smembers(self, key: str) -> set:
        return await self.redis.smembers(key)
    
    async def sismember(self, key: str, value: str) -> bool:
        return await self.redis.sismember(key, value)


redis_client = RedisClient()