# coding: utf-8
from __future__ import unicode_literals
from gevent.monkey import patch_all
patch_all()

import gevent
import logging
from gevent.pool import Pool
from redis import StrictRedis
from importlib import import_module
from slackclient import SlackClient

from settings import APPS, SLACK_TOKEN, REDIS_URL


pool = Pool(20)

CMD_PREFIX = '!'
logger = logging.getLogger()


class RedisBrain(object):
    def __init__(self):
        self.redis = None
        if REDIS_URL:
            try:
                self.redis = StrictRedis(host=REDIS_URL)
            except Exception as e:
                logger.error(e)

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
            docs.append(
                '!%s: %s' % (', '.join(app.run.commands), app.run.__doc__)
            )
            for command in app.run.commands:
                apps[command] = app

        return apps, docs

    def handle_messages(self, messages):
        for channel, user, text in messages:
            command, payloads = self.extract_command(text)
            if not command:
                continue

            app = self.apps.get(command, None)
            if not app:
                continue

            pool.apply_async(
                func=app.run, args=(self, channel, user, payloads)
            )

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
        if CMD_PREFIX != text[0]:
            return (None, None)

        tokens = text.split(' ', 1)
        if 1 < len(tokens):
            return tokens[0][1:], tokens[1]
        else:
            return (text[1:], '')

    def rtm_connect(self):
        conn = None
        try:
            conn = self.client.rtm_connect()
        except Exception as e:
            logger.error(e)
        return conn

    def read_message(self):
        events = None
        try:
            events = self.client.rtm_read()
        except Exception as e:
            logger.error(e)
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
                self.handle_messages(messages)
            gevent.sleep(0.3)


if '__main__' == __name__:
    robot = Robot()
    robot.run()
