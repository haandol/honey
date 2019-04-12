from .decorators import on_command


HELP_MSG = [
    '지금까지 메모한 내용들...',
    '='*20,
    '%s',
    '='*20,
    '메모해야 할 내용이 있으면 \'!메모 [이름] [내용]\' 이라고 해주세요.',
    '메모할 내용에 띄어쓰기를 넣으려면 내용을 큰따옴표(")로 감싸주세요.',
    '메모한 내용을 알고 싶으면 \'!메모 [이름]\' 이라고 해주세요.'
]
BRAIN_KEY = 'brain_key'


async def update_brain_key(brain, key):
    keys = await brain.get(BRAIN_KEY)
    if keys:
        L = set(keys.split(','))
        if key not in L:
            L.add(key)
    else:
        L = [key]
    await brain.set(BRAIN_KEY, ','.join(L))


@on_command(['ㅁㅁ', '메모', 'memo'])
async def run(robot, channel, user, tokens):
    '''전자두뇌에 무언가를 메모해둡니다'''
    token_count = len(tokens)

    if token_count < 1:
        keys = await robot.brain.get(BRAIN_KEY)
        if not keys:
            keys = '메모해둔 내용이 없습니다.'
        return channel, '\n'.join(HELP_MSG) % keys

    key = tokens[0]
    if token_count == 1:
        value = await robot.brain.get(key)
        message = value if value else ('%s? 처음 듣는 말이네요.' % key)
    else:
        value = tokens[1]
        await update_brain_key(robot.brain, key)
        await robot.brain.set(key, value)
        message = '메모해두었습니다.\n%s: %s' % (key, value)
    return channel, message
