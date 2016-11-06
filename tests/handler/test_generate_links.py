#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mock import Mock
import time
import json
import reader_api.config as config

import reader_api.token_generator as generator

import responses
from reader_api.handler import generate_links as handler
from reader_api.handler.constants import OPERATION, TITLE, ARTICLE_ID, USER_ID, MARK_AS_READ, MARK_AS_UNREAD


class TestGenerateLinksHandler(unittest.TestCase):

    def setUp(self):
        self.generator = Mock()
        handler.token_generator = self.generator

    @responses.activate
    def test_generate_links(self):
        # given
        event = {
            'articles': [
                {
                    'id': 123,
                    'user_id': 321,
                    'title': 'my great article',
                    'operation': 'mark_as_read'
                },
                {
                    'id': 124,
                    'user_id': 421,
                    'title': 'my another great article',
                    'operation': 'keep_unread'
                }
            ]
        }
        self.generator.encode.return_value = 'a'

        # when
        links = handler.handle(event)

        # then
        # check token generator got called
        self.assertTrue(self.generator.encode.called)
        self.assertEqual(2, len(links))

