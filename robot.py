import asyncio
import logging
import traceback
import aioredis
from async_timeout import timeout
from importlib import import_module
from slackclient import SlackClient

from settings import (
    APPS, CMD_PREFIX, CMD_LENGTH, SLACK_TOKEN, REDIS_URL,
)


logger = logging.getLogger('honey')
logger.setLevel(logging.INFO)

log_file_handler = logging.FileHandler('honey.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)


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


class Robot(object):
    def __init__(self):
        self.client = SlackClient(SLACK_TOKEN)
        self.brain = RedisBrain()
        self.apps, self.docs = self.load_apps()

    def load_apps(self):
        docs = ['='*14, 'Usage', '='*14]
        apps = {}

        for name in APPS:
            app = import_module('apps.%s' % name)
            docs.append('{0}{1}: {2}'.format(
                CMD_PREFIX, ', '.join(app.run.commands), app.run.__doc__
            ))
            for command in app.run.commands:
                apps[command] = app

        return apps, docs

    async def handle_message(self, message):
        channel, user, text = message

        command, payloads = self.extract_command(text)
        if not command:
            return

        app = self.apps.get(command, None)
        if not app:
            return

        try:
            await app.run(self, channel, user, payloads)
        except:
            traceback.print_exc()

    def extract_messages(self, events):
        messages = []
        for event in events:
            channel = event.get('channel', '')
            user = event.get('user', '')
            text = event.get('text', '')
            if channel and user and text:
                messages.append((channel, user, text))
        return messages

    def extract_command(self, text):
        if CMD_PREFIX and CMD_PREFIX != text[0]:
            return (None, None)

        tokens = text.split(' ', 1)
        if 1 < len(tokens):
            return tokens[0][CMD_LENGTH:], tokens[1]
        else:
            return (text[CMD_LENGTH:], '')

    async def rtm_connect(self, timeout_secs=10):
        logger.info('RTM Connecting...')
        try:
            async with timeout(timeout_secs):
                while not self.client.server.connected:
                    try:
                        self.client.rtm_connect(with_team_state=False)
                    except:
                        logger.error(traceback.format_exc())
                    await asyncio.sleep(1)
        except asyncio.TimeoutError as e:
            logger.error(traceback.format_exc())
            raise e
        logger.info('RTM Connected.')

    async def read_message(self):
        try:
            return self.client.rtm_read()
        except:
            logger.error(traceback.format_exc())
            # try to recover connection
            await self.rtm_connect()

    async def run(self):
        await self.brain.connect()
        await self.rtm_connect()
        if not self.client.server.connected:
            raise RuntimeError(
                'Can not connect to slack client. Check your settings.'
            )

        while True:
            events = await self.read_message()
            if events:
                messages = self.extract_messages(events)
                if messages:
                    tasks = [asyncio.ensure_future(self.handle_message(message))
                             for message in messages]
                    await asyncio.gather(*tasks)
            await asyncio.sleep(0.3)

    async def disconnect(self):
        self.brain.disconnect()
        self.client.server.websocket.close()
        logger.info('RTM disconnected.')


if '__main__' == __name__:
    robot = Robot()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(robot.run())
    finally:
        robot.disconnect()
        loop.close()
        logger.info('Honey Shutdown.')
