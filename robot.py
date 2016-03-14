# coding: utf-8
from __future__ import unicode_literals

import gevent
import logging
from gevent.pool import Pool
from gevent.monkey import patch_all
patch_all()

from redis import StrictRedis
from importlib import import_module
from slackclient import SlackClient

from settings import APPS, SLACK_TOKEN, REDIS_URL


pool = Pool(20)

CMD_PREFIX = '!'
logger = logging.getLogger()


class RedisBrain(object):
    def __init__(self, redis_url):
        try:
            self.redis = StrictRedis(host=redis_url)
        except Exception as e:
            logger.error(e)
            self.redis = None

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


class Robot(object):
    def __init__(self):
        self.client = SlackClient(SLACK_TOKEN)
        self.brain = RedisBrain(REDIS_URL)
        self.apps, self.docs = self.load_apps()

    def load_apps(self):
        docs = ['='*14, '홍모아 사용방법', '='*14]
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
        for channel, text in messages:
            command, payloads = self.extract_command(text)
            if not command:
                continue

            app = self.apps.get(command, None)
            if not app:
                continue

            pool.apply_async(func=app.run, args=(self, channel, payloads))

    def extract_messages(self, events):
        messages = []
        for e in events:
            channel = e.get('channel', '')
            text = e.get('text', '')
            if channel and text:
                messages.append((channel, text))
        return messages

    def extract_command(self, text):
        if CMD_PREFIX != text[0]:
            return (None, None)

        tokens = text.split(' ', 1)
        if 1 < len(tokens):
            return tokens[0][1:], tokens[1]
        else:
            return (text[1:], '')

    def run(self):
        if self.client.rtm_connect():
            while True:
                events = self.client.rtm_read()
                if events:
                    messages = self.extract_messages(events)
                    self.handle_messages(messages)
                gevent.sleep(1)


if '__main__' == __name__:
    robot = Robot()
    robot.run()
