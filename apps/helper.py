# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command


@on_command(['도움', 'help'])
def run(robot, channel, tokens):
    '''print stringdocs of each function'''
    return '\n'.join(robot.docs)
