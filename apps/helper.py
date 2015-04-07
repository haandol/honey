# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command


@on_command(['도움', 'help'])
def run(robot, channel, tokens):
    '''도움말을 출력'''
    return '\n'.join(robot.docs)
