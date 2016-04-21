# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command


@on_command(['ㄷㅇ', '도움', 'help'])
def run(robot, channel, user, tokens):
    '''도움말을 출력해드려요'''
    return channel, '\n'.join(robot.docs)
