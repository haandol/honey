# coding: utf-8
from __future__ import unicode_literals, print_function

import traceback
from itertools import imap
from functools import wraps


def _is_contain_command(commands, message):
    trigger = message.startswith
    return any(
        imap(trigger, ('!'+c.strip() for c in commands))
    )


def _extract_tokens(message):
    tokens = message.split()
    return tokens[1:] if len(tokens) > 1 else []


def on_command(commands):
    def decorator(func):
        func.commands = commands

        @wraps(func)
        def _decorator(client, channel, message):
            if commands and _is_contain_command(commands, message):
                tokens = _extract_tokens(message)
                try:
                    message = func(client, channel, tokens)
                    client.rtm_send_message(channel, message)
                    return message
                except:
                    print('[Error] 다음이유로 메시지를 전달하지 못했습니다.')
                    traceback.print_exc()
                    print('')
                    return None
            return ''
        return _decorator
    return decorator
