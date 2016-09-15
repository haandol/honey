# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command


HELP_MSG = [
    '#general 에 대신 써줬으면 하는 말이 있으면 \'!대필 [내용]\' 이라고 해주세요.',
    '내용에 띄어쓰기가 들어있다면 내용을 큰따옴표로 감싸주세요.',
    '다른 채널에 써줬으면 한다면 \'!대필 [채널명] [내용]\' 이라고 해주세요.'
]


@on_command(['ㄷㅍ', '대필', 'ghost'])
def run(robot, channel, user, tokens):
    '''특정 채널 또는 general 채널에 글을 대신 써줍니다.'''
    if len(tokens) < 1:
        return channel, '\n'.join(HELP_MSG)

    if len(tokens) == 1:
        return 'general', ' '.join(tokens)
    else:
        return tokens[0], ' '.join(tokens[1:])
