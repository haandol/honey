# coding: utf-8
from __future__ import unicode_literals

import re
import traceback
from functools import wraps


TOKENIZE_PATTERN = re.compile(r'["“](.+?)["”]|(\S+)', re.U | re.S)


def _extract_tokens(message):
    '''Parse the given message, extract command and split'em into tokens

        Args:
            message (str): user gave message

        Returns:
            (list): tokens
    '''
    return filter(lambda x: x and x.strip(), TOKENIZE_PATTERN.split(message))


def on_command(commands):
    def decorator(func):
        func.commands = commands

        @wraps(func)
        def _decorator(*args, **kwargs):
            robot, channel, user, message = args
            if commands:
                tokens = _extract_tokens(message)
                try:
                    channel, message = func(robot, channel, user, tokens)
                    if channel:
                        robot.client.rtm_send_message(channel, message)
                        return message
                    else:
                        print "[Warn] Couldn't delivered a message"
                except:
                    print "[Error] Couldn't delivered the message"
                    traceback.print_exc()
                    print
                    return None
            return ''
        return _decorator
    return decorator
