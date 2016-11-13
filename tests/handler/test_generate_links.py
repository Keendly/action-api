#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mock import Mock

import responses
from reader_api.handler import generate_links as handler


class TestGenerateLinksHandler(unittest.TestCase):

    def setUp(self):
        self.generator = Mock()
        handler.token_generator = self.generator

    @responses.activate
    def test_generate_links(self):
        # given
        event = {
            'articles': {
                '123': [
                    {
                        'userId': 321,
                        'title': 'my great article',
                        'operation': 'mark_as_read'
                    }
                ],
                '124': [
                    {
                        'userId': 421,
                        'title': 'my another great article',
                        'operation': 'keep_unread'
                    }
                ]
            }
        }
        self.generator.encode.return_value = 'a'

        # when
        links = handler.handle(event)

        # then
        # check token generator got called
        self.assertTrue(self.generator.encode.called)
        self.assertEqual(2, len(links))

    def test_generate_links_multiple_actions_for_article(self):
        # given
        event = {
            'articles': {
                '123': [
                    {
                        'userId': 321,
                        'title': 'my great article',
                        'operation': 'mark_as_read'
                    },
                    {
                        'userId': 421,
                        'title': 'my another great article',
                        'operation': 'keep_unread'
                    }
                ]
            }
        }
        self.generator.encode.return_value = 'a'

        # when
        links = handler.handle(event)

        # then
        # check token generator got called
        self.assertTrue(self.generator.encode.called)
        self.assertEqual(1, len(links))
        self.assertEqual(2, len(links['123']))
