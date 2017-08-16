# coding: utf-8
from __future__ import unicode_literals

# https://{$YOUR_TEAM}.slack.com/apps/manage/custom-integrations
SLACK_TOKEN = 'Set token for your slack-bot'

# set redis url if you want to enable redis related functions like redis_brain
REDIS_URL = None
REDIS_PORT = 6379

# command prefix
CMD_PREFIX = '!'
CMD_LENGTH = len(CMD_PREFIX)

# gevent pool size
POOL_SIZE = 20

# add your app name to this list
APPS = ['hello_world', 'helper', 'giphy', 'ghost']
