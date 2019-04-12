import re
import traceback
from functools import wraps
from loggers import logger


TOKENIZE_PATTERN = re.compile(r'["“](.+?)["”]|(\S+)', re.U | re.S)


def _extract_tokens(message):
    '''Parse the given message, extract command and split'em into tokens

        Args:
            message (str): user gave message

        Returns:
            (list): tokens
    '''
    return list(filter(lambda x: x and x.strip(), TOKENIZE_PATTERN.split(message)))


def on_command(commands):
    def decorator(func):
        func.commands = commands

        @wraps(func)
        async def _decorator(robot, channel, user, message):
            if commands:
                tokens = _extract_tokens(message)
                try:
                    channel, message = await func(robot, channel, user, tokens)
                    logger.debug('[Debug] message: {}'.format(message))
                    if channel:
                        if dict == type(message) and 'text' in message:
                            robot.client.api_call(
                                'chat.postMessage', channel=channel, **message
                            )
                        else:
                            robot.client.rtm_send_message(channel, str(message))
                        return message
                    else:
                        logger.warning('Can not send to empty channel')
                except:
                    logger.error('Can not deliver the message because...')
                    traceback.print_exc()
            return None
        return _decorator
    return decorator
