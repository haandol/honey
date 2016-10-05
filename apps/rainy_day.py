# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command

import requests
from bs4 import BeautifulSoup as Soup


URL = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1162057500'

DAY_STR = ('오늘', '내일', '모레')


@on_command(['ㅂㅇ', '비와', 'rain'])
def run(robot, channel, user, tokens):
    '''3일 이내에 비가 오는지 여부를 알려드립니다.'''
    res = requests.get(URL).text
    soup = Soup(res, features='xml')
    data = soup.body.find_all('data')
    for each in data:
        day_diff = each.day.text
        if '비' in each.wfKor.text:
            return channel, '%s %s시부터 비가 올예정입니다.' % (DAY_STR[int(day_diff)], each.hour.text)
    return channel, '이틀 이내에는 비가 오지 않습니다.'
