#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time
import json
import reader_api.config as config

import reader_api.token_generator as generator

import responses
from reader_api.handler import execute_action as handler
from reader_api.handler.constants import OPERATION, TITLE, ARTICLE_ID, USER_ID, MARK_AS_READ, MARK_AS_UNREAD


class TestExecuteActionHandler(unittest.TestCase):

    def setUp(self):
        config.config = {
            'feeds_client_id': 'feeds_api_client_id',
            'feeds_client_secret': 'feeds_api_client_secret',
            'token_secret': 'reader_api_token_secret'
        }

    @responses.activate
    def test_handle_mark_read(self):
        # given
        auth_token = 'my_auth_token'
        action_token = generator.encode({
            OPERATION: MARK_AS_READ,
            TITLE: 'my awesome article',
            ARTICLE_ID: 123,
            USER_ID: 431
        })

        responses.add(responses.POST, 'https://app.keendly.com/auth',
                      json={
                          "expiresIn": "3600",
                          "tokeType": "Bearer",
                          "scope": "read",
                          "accessToken": auth_token
                      }, status=200)

        responses.add(responses.POST, 'https://app.keendly.com/api/feeds/markArticleRead',
                      status=200)

        # when
        ret = handler.handle({
            'queryStringParameters': {
                'action': action_token
            }
        })

        # then
        # check bearer token requested
        self.assertEqual({
            "token": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQzMX0.mh6pREHAfXn_4LRo7eeDYKbepqHuFGOZz-RXRCL9J9w',
            "grant_type": "bearer",
            "client_id": 'feeds_api_client_id'
        }, json.loads(responses.calls[0].request.body))

        # check returned token used in authorization header
        self.assertEqual('Bearer ' + auth_token, responses.calls[1].request.headers['Authorization'])

        # check article id passed to mark as read endpoint
        self.assertEqual([123], json.loads(responses.calls[1].request.body))

        # check return content
        self.assertEqual(200, ret['statusCode'])
        self.assertTrue('successfully' in ret['body'])
        self.assertTrue('my awesome article' in ret['body'])

    @responses.activate
    def test_handle_mark_read_error(self):
        # given
        auth_token = 'my_auth_token'
        action_token = generator.encode({
            OPERATION: MARK_AS_READ,
            TITLE: 'my awesome article',
            ARTICLE_ID: 123,
            USER_ID: 431
        })

        responses.add(responses.POST, 'https://app.keendly.com/auth',
                      json={
                          "expiresIn": "3600",
                          "tokeType": "Bearer",
                          "scope": "read",
                          "accessToken": auth_token
                      }, status=200)

        responses.add(responses.POST, 'https://app.keendly.com/api/feeds/markArticleRead',
                      status=500)

        # when
        ret = handler.handle({
            'queryStringParameters': {
                'action': action_token
            }
        })

        # then
        self.assertEqual(200, ret['statusCode'])
        self.assertTrue('sorry' in ret['body'])

    @responses.activate
    def test_handle_keep_unread(self):
        # given
        auth_token = 'my_auth_token'
        action_token = generator.encode({
            OPERATION: MARK_AS_UNREAD,
            TITLE: 'my awesome article',
            ARTICLE_ID: 123,
            USER_ID: 431
        })

        responses.add(responses.POST, 'https://app.keendly.com/auth',
                      json={
                          "expiresIn": "3600",
                          "tokeType": "Bearer",
                          "scope": "read",
                          "accessToken": auth_token
                      }, status=200)

        responses.add(responses.POST, 'https://app.keendly.com/api/feeds/markArticleUnread',
                      status=200)

        # when
        ret = handler.handle({
            'queryStringParameters': {
                'action': action_token
            }
        })

        # then
        # check bearer token requested
        self.assertEqual({
            "token": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQzMX0.mh6pREHAfXn_4LRo7eeDYKbepqHuFGOZz-RXRCL9J9w',
            "grant_type": "bearer",
            "client_id": 'feeds_api_client_id'
        }, json.loads(responses.calls[0].request.body))

        # check returned token used in authorization header
        self.assertEqual('Bearer ' + auth_token, responses.calls[1].request.headers['Authorization'])

        # check article id passed to mark as read endpoint
        self.assertEqual([123], json.loads(responses.calls[1].request.body))

        # check return content
        self.assertEqual(200, ret['statusCode'])
        self.assertTrue('successfully' in ret['body'])
        self.assertTrue('my awesome article' in ret['body'])

    def test_handle_token_expired(self):
        # given
        generator.TOKEN_EXPIRATION_IN_SECONDS = 1
        auth_token = 'my_auth_token'
        action_token = generator.encode({
            OPERATION: MARK_AS_READ,
            TITLE: 'my awesome article',
            ARTICLE_ID: 123,
            USER_ID: 431
        })

        responses.add(responses.POST, 'https://app.keendly.com/auth',
                      json={
                          "expiresIn": "3600",
                          "tokeType": "Bearer",
                          "scope": "read",
                          "accessToken": auth_token
                      }, status=200)

        responses.add(responses.POST, 'https://app.keendly.com/api/feeds/markArticleRead',
                      status=200)

        # when
        time.sleep(2) # wait for token to expire
        ret = handler.handle({
            'queryStringParameters': {
                'action': action_token
            }
        })

        # then
        self.assertEqual(200, ret['statusCode'])
        self.assertTrue('expired' in ret['body'])

    def test_handle_bad_token(self):
        # given
        responses.add(responses.POST, 'https://app.keendly.com/auth',
                      json={
                          "expiresIn": "3600",
                          "tokeType": "Bearer",
                          "scope": "read",
                          "accessToken": 'my_auth_token'
                      }, status=200)

        # when
        ret = handler.handle({
            'queryStringParameters': {
                'action': 'some completely wrong token'
            }
        })

        # then
        self.assertEqual(200, ret['statusCode'])
        self.assertTrue('sorry' in ret['body'])

