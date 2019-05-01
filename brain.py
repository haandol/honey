import time
import redis
import traceback
from loggers import logger
from settings import REDIS_URL, REDIS_PORT, MAX_CONNECTION


class RedisBrain(object):
    def __init__(self):
        self.redis = None

    def connect(self):
        if not REDIS_URL:
            logger.info('No brain on this bot.')
            return

        logger.info('Brain Connecting...')
        try:
            pool = redis.ConnectionPool(
                host=REDIS_URL, port=REDIS_PORT,
                max_connections=MAX_CONNECTION, db=0
            )
            self.redis = redis.Redis(connection_pool=pool)
            self.redis.set('foo', 'bar')
            logger.info('Brain Connected: {}'.format(REDIS_URL))
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

    def set(self, key, value):
        if not self.redis:
            return False

        self.redis.set(key, value)
        return True

    def get(self, key):
        if not self.redis:
            return None

        value = self.redis.get(key)
        return value.decode('utf-8') if value else ''

    def lpush(self, key, value):
        if not self.redis:
            return False

        self.redis.lpush(key, value)
        return True

    def lpop(self, key):
        if not self.redis:
            return None

        value = self.redis.lpop(key)
        return value.decode('utf-8') if value else ''