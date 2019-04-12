import asyncio
import aioredis
import traceback
from loggers import logger
from settings import REDIS_URL
from async_timeout import timeout


class RedisBrain(object):
    def __init__(self):
        self.redis = None

    async def connect(self, timeout_secs=10):
        if not REDIS_URL:
            logger.info('No brain on this bot.')
            return
        
        logger.info('Brain Connecting...')
        try:
            async with timeout(timeout_secs):
                while not self.redis:
                    try:
                        self.redis = await aioredis.create_redis(REDIS_URL)
                    except:
                        logger.error(traceback.format_exc())
                    await asyncio.sleep(1)
        except asyncio.TimeoutError as e:
            logger.error(traceback.format_exc())
            raise e
        logger.info('Brain Connected: {}'.format(REDIS_URL))

    async def set(self, key, value):
        if not self.redis:
            return False

        await self.redis.set(key, value)
        return True

    async def get(self, key):
        if not self.redis:
            return None

        value = await self.redis.get(key)
        return value.decode('utf-8') if value else ''

    async def lpush(self, key, value):
        if not self.redis:
            return False

        await self.redis.lpush(key, value)
        return True

    async def lpop(self, key):
        if not self.redis:
            return None

        value = await self.redis.lpop(key)
        return value.decode('utf-8') if value else ''

    def disconnect(self):
        if not self.redis:
            return

        self.redis.close()
        logger.info('Brain disconnected.')