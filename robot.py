# coding: utf-8
from __future__ import unicode_literals
from gevent.monkey import patch_all
patch_all()

import gevent
import logging
import traceback
from gevent.pool import Pool
from redis import StrictRedis
from importlib import import_module
from slackclient import SlackClient

from settings import (
    APPS, CMD_PREFIX, CMD_LENGTH, SLACK_TOKEN, REDIS_URL, POOL_SIZE
)


pool = Pool(POOL_SIZE)

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
        if REDIS_URL:
            try:
                self.redis = StrictRedis(host=REDIS_URL)
            except:
                logger.error(traceback.format_exc())

    def set(self, key, value):
        if self.redis:
            self.redis.set(key, value)
            return True
        else:
            return False

    def get(self, key):
        if self.redis:
            return self.redis.get(key)
        return None

    def lpush(self, key, value):
        if self.redis:
            self.redis.lpush(key, value)
            return True
        else:
            return False

    def lpop(self, key):
        if self.redis:
            return self.redis.lpop(key)
        return None

    def lindex(self, key):
        if self.redis:
            return self.redis.lindex(key)
        return None


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

    def handle_message(self, message):
        channel, user, text = message

        command, payloads = self.extract_command(text)
        print command, payloads
        if not command:
            return

        app = self.apps.get(command, None)
        if not app:
            return

        try:
            pool.apply_async(func=app.run,
                             args=(self, channel, user, payloads))
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

    def rtm_connect(self):
        conn = None
        try:
            conn = self.client.rtm_connect()
        except:
            logger.error(traceback.format_exc())
        else:
            return conn

    def read_message(self):
        events = None
        try:
            events = self.client.rtm_read()
        except:
            logger.error(traceback.format_exc())
            self.rtm_connect()
        return events

    def run(self):
        if not self.rtm_connect():
            raise RuntimeError(
                'Can not connect to slack client. Check your settings.'
            )

        while True:
            events = self.read_message()
            if events:
                messages = self.extract_messages(events)
                for message in messages:
                    self.handle_message(message)
            gevent.sleep(0.3)


if '__main__' == __name__:
    robot = Robot()
    robot.run()
