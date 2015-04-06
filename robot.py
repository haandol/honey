# coding: utf-8
from __future__ import unicode_literals

import time
from importlib import import_module
from slackclient import SlackClient

from settings import APPS, SLACK_TOKEN


class Robot(object):
    def __init__(self):
        self.client = SlackClient(SLACK_TOKEN)
        self.apps = self.load_apps()

    def load_apps(self):
        self.client.docs = []
        self.client.docs.append('='*14)
        self.client.docs.append('홍모아 사용방법')
        self.client.docs.append('='*14)

        apps = {}
        for name in APPS:
            app = import_module('apps.%s' % name)
            apps[name] = app

            doc = '!%s: %s' % (', '.join(app.run.commands), app.run.__doc__)
            self.client.docs.append(doc)

        return apps

    def handle_messages(self, messages):
        # TODO: text를 미리 보고 필요한 함수만 실행하도록 수정
        for channel, text in messages:
            for name in self.apps:
                self.apps[name].run(self.client, channel, text)

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
                time.sleep(1)


if '__main__' == __name__:
    robot = Robot()
    robot.run()
