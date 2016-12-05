
# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command

from gevent.monkey import patch_all
patch_all()

import re
import random
import requests
from urllib2 import unquote

from __init__ import build_message


HELP_MSG = [
    'giphy 에서 움짤을 검색하고 싶으면 \'!움짤 [검색어]\' 이라고 해주세요.',
    '검색어는 `영어`만 됩니다. 검색어에 띄어쓰기가 들어있다면 큰따옴표로 감싸주세요.',
]

URL = 'http://api.giphy.com/v1/gifs/search?'


def get_giphy_message(query):
    params = {
        'q': query,
        'api_key': 'dc6zaTOxFJmzC',
        'offset': random.randint(0, 1024),
        'limit': 1,
    }

    try:
        result = requests.get(URL, params=params).json()
    except:
        message = 'Could not connected to giphy.com. Try again later.'
    else:
        if result['pagination']['count'] < 1:
            message = 'No result found for "%s".' % query
        else:
            el = result['data'][0]
            image_url = el['images']['original']['url']

            attachments = [
                {'text': unquote(query), 'image_url': image_url}
            ]
            message = build_message(
                text=query, attachments=attachments
            )
    return message


@on_command(['ㄱㅍ', '움짤', 'gif', 'giphy'])
def run(robot, channel, user, tokens):
    '''Search a random image from giphy.com.'''
    if 1 != len(tokens):
        return channel, '\n'.join(HELP_MSG)

    query = tokens[0]
    if re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', query, re.U):
        return channel, 'Only English query is avaliable for giphy.com.'

    message = get_giphy_message(query)
    return channel, message


if '__main__' == __name__:
    print get_giphy_message('funny cat')
