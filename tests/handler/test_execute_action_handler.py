#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mock import Mock, call
import jwt
import responses
from reader_api.handler import execute_action_handler as handler

class TestExecuteActionHandler(unittest.TestCase):

    def setUp(self):
        self.config = mocked_config()
        handler.config = self.config

    @responses.activate
    def test_handle_mark_read(self):
        # given
        #action =

        # then
        handler.handle({
            ''
        })


    def test_handle_keep_unread(self):
        pass

    def test_handle_token_expired(self):
        pass

    def test_handle_bad_token(self):
        pass

    def test_handle_no_token(self):
        # when
        res = handler.handle({})

        # then


def mocked_config():
    config = Mock()
    def config_get(key):
        return {
            'feeds_client_id': 'ala',
            'feeds_client_secret': 'ma',
            'token_secret': 'kota'
        }[key]

    config.get.side_effect = config_get
    return config
