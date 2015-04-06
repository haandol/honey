# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command


@on_command(['도움', 'help'])
def run(client, channel, tokens):
    '''도움말을 출력'''
    return '\n'.join(client.docs)
