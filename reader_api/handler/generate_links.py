#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import boto3
from random import choice
from string import ascii_uppercase
import reader_api.token_generator as token_generator
from reader_api.handler.constants import OPERATION, TITLE, ARTICLE_ID, USER_ID, MARK_AS_READ, MARK_AS_UNREAD, \
    MARK_AS_READ_TEXT, MARK_AS_UNREAD_TEXT
from reader_api.config import SELF_URL

# according to http://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dg-limits.html
MAX_RESULT_SIZE = 32000


def handle(event):
    links = {}
    for id, actions in event['articles'].iteritems():
        for action in actions:
            link = generate_link({
                TITLE: action['title'],
                ARTICLE_ID: id,
                USER_ID: action['userId'],
                OPERATION: _translate_operation(action['operation'])
            })
            res = {
                'action': _to_text(action['operation']),
                'link': link
            }
            if id in links:
                links[id].append(res)
            else:
                links[id] = [res]

    if len(json.dumps(links)) > MAX_RESULT_SIZE:
        js = json.dumps(links)
        key = _store_links('keendly', js)
        return {
            's3Links': {
                'bucket': 'keendly',
                'key': key
            }
        }
    else:
        return {
            'links': links
        }

def _store_links(bucket, content):
    key = 'messages/' + ''.join(choice(ascii_uppercase) for i in range(12)) + '.json'
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).put_object(Key=key, Body=content)
    return key

def _translate_operation(operation):
    if operation == 'mark_as_read':
        return MARK_AS_READ
    return MARK_AS_UNREAD

def _to_text(operation):
    if operation == 'mark_as_read':
        return MARK_AS_READ_TEXT
    return MARK_AS_UNREAD_TEXT


def generate_link(payload):
    token = token_generator.encode(payload)
    return SELF_URL + token

