# coding: utf-8
from __future__ import unicode_literals

import gevent
from gevent.pool import Pool
from gevent.monkey import patch_all; patch_all()

from redis import StrictRedis
from importlib import import_module
from slackclient import SlackClient

from settings import APPS, SLACK_TOKEN, REDIS_URL


pool = Pool(20)


class RedisBrain(object):
    def __init__(self, redis_url):
        try:
            self.redis = StrictRedis(host=redis_url, port=7777, db=0)
        except:
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
        self.docs = []
        self.brain = RedisBrain(REDIS_URL)
        self.apps = self.load_apps()

    def load_apps(self):
        self.docs.append('='*14)
        self.docs.append('홍모아 사용방법')
        self.docs.append('='*14)

        apps = {}
        for name in APPS:
            app = import_module('apps.%s' % name)
            apps[name] = app

            doc = '!%s: %s' % (', '.join(app.run.commands), app.run.__doc__)
            self.docs.append(doc)

        return apps

    def handle_messages(self, messages):
        # TODO: text를 미리 보고 필요한 함수만 실행하도록 수정
        params = [(self, channel, text)
                  for channel, text in messages
                  if text.startswith('!')]
        if params:
            for name in self.apps:
                pool.imap_unordered(self.apps[name].run, params)

    def extract_messages(self, events):
        messages = []
        for e in events:
            channel = e.get('channel', '')
            text = e.get('text', '')
            if channel and text:
                messages.append((channel, text))
        return messages

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
