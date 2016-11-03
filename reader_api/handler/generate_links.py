#!/usr/bin/env python
# -*- coding: utf-8 -*-

import reader_api.token_generator as token_generator
from reader_api.handler.constants import OPERATION, TITLE, ARTICLE_ID, USER_ID, MARK_AS_READ, MARK_AS_UNREAD

# TODO fix
#SELF_URL = 'https://api.keendly.com/reader?action='
SELF_URL = 'http://localhost:5000/execute?action='


def handle(event):
    links = []
    for article in event['articles']:
        link = generate_link({
            TITLE: article['title'],
            ARTICLE_ID: article['id'],
            USER_ID: article['user_id'],
            OPERATION: _translate_operation(article['operation'])
        })
        # only one action per article supported
        links.append(link)
    return links


def _translate_operation(operation):
    if operation == 'mark_as_read':
        return MARK_AS_READ
    return MARK_AS_UNREAD


def generate_link(payload):
    token = token_generator.encode(payload)
    return SELF_URL + token

