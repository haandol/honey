# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command


@on_command(['하이', 'hi'])
def run(robot, channel, tokens):
    '''헬로월드를 출력'''
    return 'hello world'
