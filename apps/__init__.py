# coding: utf-8
from __future__ import unicode_literals


def build_message(text='', attachments=[], unfurl_media=True, as_user=True):
    message = {
        'text': text,
        'as_user': as_user,
        'unfurl_media': unfurl_media,
    }
    if attachments:
        message.update({'attachments': attachments})
    return message
