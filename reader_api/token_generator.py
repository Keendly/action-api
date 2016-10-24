#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import jwt

import config

TOKEN_EXPIRATION_TIME = 2 #days
TOKEN_EXPIRATION_IN_SECONDS = 60 * 60 * 24 * TOKEN_EXPIRATION_TIME

def encode(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_EXPIRATION_IN_SECONDS)
    return jwt.encode(payload, config.get('token_secret'), algorithm='HS256')


def decode(token):
    return jwt.decode(token, config.get('token_secret'))


def generate_token(user_id, article_id, title, action):
    payload = {
              'exp': 'a',
      'u': user_id,
   'id': article_id,
     't': title,
      'a': action
    }


