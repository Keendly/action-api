#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import json
from random import choice
from string import ascii_uppercase
import reader_api.token_generator as token_generator
from reader_api.handler.constants import OPERATION, TITLE, ARTICLE_ID, USER_ID, MARK_AS_READ, MARK_AS_UNREAD, \
    MARK_AS_READ_TEXT, MARK_AS_UNREAD_TEXT, SAVE_ARTICLE, SAVE_TEXT
from reader_api.config import SELF_URL

# according to http://docs.aws.amazon.com/amazonswf/latest/developerguide/swf-dg-limits.html
MAX_RESULT_SIZE = 32000


def handle(event):
    links = {}
    if event.get('s3Articles') is not None:
        articles = _get_articles('keendly', event['s3Articles'])
        event['articles'] = json.loads(articles)

    for id, actions in event['articles'].iteritems():
        for action in actions:
            link = generate_link({
                TITLE: action['title'],
                ARTICLE_ID: id,
                USER_ID: event.get('userId') or action.get('userId'),
                OPERATION: _translate_operation(action['operation'])
            })
            res = {
                'action': _to_text(action['operation'], event.get('provider')),
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

def _get_articles(bucket, key):
    s3 = boto3.resource('s3')
    file_name = _random_name()
    file_path = '/tmp/' + file_name
    s3.meta.client.download_file(bucket, key, file_path)
    f = open(file_path, "rb")
    msg = f.read()
    f.close()
    return msg

def _random_name():
    return ''.join(choice(ascii_uppercase) for i in range(12))

def _translate_operation(operation):
    if operation == 'mark_as_read':
        return MARK_AS_READ
    elif operation == 'save_article':
        return SAVE_ARTICLE
    return MARK_AS_UNREAD

def _to_text(operation, provider):
    if operation == 'mark_as_read':
        return MARK_AS_READ_TEXT
    elif operation == 'save_article':
        if provider.lower() in SAVE_TEXT:
            return SAVE_TEXT[provider.lower()]
        else:
            return SAVE_TEXT['default']
    return MARK_AS_UNREAD_TEXT


def generate_link(payload):
    token = token_generator.encode(payload)
    return SELF_URL + token

