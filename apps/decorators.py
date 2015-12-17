# coding: utf-8
from __future__ import unicode_literals

import re
import traceback
from functools import wraps


def _is_contain_command(commands, message):
    '''check if there is a command in message

        Args:
            commands (list): list of command for the specific function
            message (str): user gave message

        Returns:
            (bool): returns True if message contains any of commands
    '''
    command = message.split()[0]
    return any((command == '!'+c.strip() for c in commands))


def _extract_tokens(message):
    '''Parse the given message, extract command and split'em into tokens

        Args:
            message (str): user gave message

        Returns:
            (list): tokens
    '''
    pattern = re.compile(r'["“](.+?)["”]|(\S+)', re.U | re.S)
    tokens = message.split(' ', 1)
    if 1 < len(tokens):
        return filter(lambda x: x and x.strip(), pattern.split(tokens[1]))
    else:
        return []


def on_command(commands):
    def decorator(func):
        func.commands = commands

        @wraps(func)
        def _decorator(args):
            robot, channel, message = args
            if commands and _is_contain_command(commands, message):
                tokens = _extract_tokens(message)
                try:
                    channel, message = func(robot, channel, tokens)
                    if channel:
                        robot.client.rtm_send_message(channel, message)
                        return message
                    else:
                        print "[Warn] Couldn't delivered a message"
                except:
                    print "[Error] Could't delivered a message for this reason"
                    traceback.print_exc()
                    print
                    return None
            return ''
        return _decorator
    return decorator
