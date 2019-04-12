from .decorators import on_command


HELP_MSG = [
    '지금까지 기억한 내용들...',
    '='*20,
    '%s',
    '='*20,
    '기억해야 할 내용이 있으면 \'!기억 [이름] [내용]\' 이라고 해주세요.',
    '기억할 내용에 띄어쓰기를 넣으려면 내용을 큰따옴표(")로 감싸주세요.',
    '기억한 내용을 알고 싶으면 \'!기억 [이름]\' 이라고 해주세요.'
]
BRAIN_KEY = 'brain_key'


async def update_brain_key(brain, key):
    keys = await brain.get(BRAIN_KEY)
    if keys:
        L = set(keys.decode('utf-8').split(','))
        if key not in L:
            L.add(key)
    else:
        L = [key]
    await brain.set(BRAIN_KEY, ','.join(L))


@on_command(['ㄱㅇ', '기억', 'memo'])
async def run(robot, channel, user, tokens):
    '''홍모아 전자두뇌에 무언가를 기억시킵니다'''
    token_count = len(tokens)

    if token_count < 1:
        keys = await robot.brain.get(BRAIN_KEY)
        if keys:
            keys = keys.decode('utf-8')
        else:
            keys = '기억한 내용이 없습니다.'
        return channel, '\n'.join(HELP_MSG) % keys

    key = tokens[0]
    if token_count == 1:
        value = await robot.brain.get(key)
        if value:
            message = '%s %s' % (key, value.decode('utf-8'))
        else:
            message = '%s? 처음 들어보는 말이네요.' % key
    else:
        value = tokens[1]
        await update_brain_key(robot.brain, key)
        await robot.brain.set(key, value)
        message = '%s %s!! 잘 기억해뒀어요.' % (key, value)
    return channel, message
