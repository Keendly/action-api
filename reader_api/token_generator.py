#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import jwt

import config

SECRET = config.get('token_secret')
TOKEN_EXPIRATION_TIME = 2 #days


def encode(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=TOKEN_EXPIRATION_TIME)
    return jwt.encode(payload, SECRET, algorithm='HS256')


def decode(token):
    return jwt.decode(token, SECRET)


def generate_token(user_id, article_id, title, action):
    payload = {
              'exp': 'a',
      'u': user_id,
   'id': article_id,
     't': title,
      'a': action
    }


