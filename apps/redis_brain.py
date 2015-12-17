# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command


HELP_MSG = [
    '제가 외워야 할 내용이 있으면 \'!기억 [이름] [내용]\' 이라고 해주세요.',
    '기억할 내용에 띄어쓰기를 넣으려면 내용을 큰따옴표(")로 감싸주세요.',
    '기억한 내용을 알고 싶으면 \'!기억 [이름]\' 이라고 해주세요.'
]


@on_command(['ㄱㅇ', '기억', 'memo'])
def run(robot, channel, tokens):
    '''홍모아 전자두뇌에 무언가를 기억시킵니다'''

    token_count = len(tokens)

    if token_count < 1:
        return channel, '\n'.join(HELP_MSG)

    key = tokens[0]
    if token_count == 1:
        value = robot.brain.get(key)
        if value:
            message = '%s %s' % (key, value.decode('utf-8'))
        else:
            message = '%s? 처음 들어보는 말이네요.' % key
    else:
        value = tokens[1]
        robot.brain.set(key, value)
        message = '%s %s!! 잘 기억해뒀어요.' % (key, value)
    return channel, message
