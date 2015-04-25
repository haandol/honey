# coding: utf-8
from __future__ import unicode_literals

import traceback
from functools import wraps


def _is_contain_command(commands, message):
    return any((message == '!'+c.strip() for c in commands))


def _extract_tokens(message):
    tokens = message.split()
    return tokens[1:] if len(tokens) > 1 else []


def on_command(commands):
    def decorator(func):
        func.commands = commands

        @wraps(func)
        def _decorator(robot, channel, message):
            if commands and _is_contain_command(commands, message):
                tokens = _extract_tokens(message)
                try:
                    message = func(robot, channel, tokens)
                    robot.client.rtm_send_message(channel, message)
                    return message
                except:
                    print '[Error] Could not delivered message because ...'
                    traceback.print_exc()
                    print
                    return None
            return ''
        return _decorator
    return decorator
