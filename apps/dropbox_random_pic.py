# coding: utf-8
"""
Pick a random image from dropbox shared app folder.

Usage:
    1. Visit: https://www.dropbox.com/developers/apps
    2. Create App - Dropbox API - App Folder
    3. Generate Access Token
    4. Assign it to ACCESS_TOKEN variable
"""
from __future__ import unicode_literals
from decorators import on_command

from gevent.monkey import patch_all
patch_all()

import random
import dropbox


ACCESS_TOKEN = None

DEFAULT_IMG = 'https://media2.giphy.com/media/26vUTlnHulTgAU7le/200w.gif'


def get_dropbox_image_paths(dbx):
    return [entry.path_lower for entry in dbx.files_list_folder('').entries]


def dropbox_random_pic():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    paths = get_dropbox_image_paths(dbx)
    if not paths:
        return DEFAULT_IMG

    path = random.choice(paths)
    metadata = dbx.sharing_create_shared_link(path)
    return metadata.url.replace('dl=0', 'raw=1').replace(
        'www.dropbox.com', 'dl.dropboxusercontent.com'
    )


@on_command(['ㅍㅍ', '펀픽', 'funpic'])
def run(robot, channel, user, tokens):
    '''드랍박스 폴더에서 랜덤 이미지를 가져와서 보여드립니다.'''
    return channel, dropbox_random_pic()
