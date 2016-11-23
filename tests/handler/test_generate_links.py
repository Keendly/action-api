#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mock import Mock, call

import responses
from reader_api.handler import generate_links as handler
from reader_api.handler.constants import OPERATION, TITLE, ARTICLE_ID, USER_ID, SAVE_ARTICLE

DEFAULT_MAX = handler.MAX_RESULT_SIZE

class TestGenerateLinksHandler(unittest.TestCase):

    def setUp(self):
        self.generator = Mock()
        handler.token_generator = self.generator
        handler.MAX_RESULT_SIZE = DEFAULT_MAX

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
        self.assertIsNotNone(links.get('links'))
        self.assertEqual(2, len(links['links']))

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
        self.assertIsNotNone(links.get('links'))
        self.assertEqual(1, len(links['links']))
        self.assertEqual(2, len(links['links']['123']))

    def test_generate_big_response(self):
        # given
        handler.MAX_RESULT_SIZE = 5

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
        self.assertTrue(self.generator.encode.called)
        self.assertIsNone(links.get('links'))
        self.assertIsNotNone(links.get('s3Links'))

    def test_generate_save_article_default_text(self):
        # given
        event = {
            'userId': 321,
            'provider': 'NEWSBLUR',
            'articles': {
                '123': [
                    {
                        'title': 'my great article',
                        'operation': 'save_article'
                    }
                ]
            }
        }
        self.generator.encode.return_value = 'a'

        # when
        links = handler.handle(event)

        # then
        self.generator.encode.assert_called_with({
            TITLE: 'my great article',
            ARTICLE_ID: '123',
            USER_ID: 321,
            OPERATION: SAVE_ARTICLE
        })
        self.assertTrue('Click to save article', links['links']['123'][0]['action'])
        self.assertEqual(1, len(links['links']))
        self.assertEqual(1, len(links['links']['123']))

    def test_generate_save_article_custom_text(self):
        # given
        event = {
            'userId': 321,
            'provider': 'INOREADER',
            'articles': {
                '123': [
                    {
                        'title': 'my great article',
                        'operation': 'save_article'
                    }
                ]
            }
        }
        self.generator.encode.return_value = 'a'

        # when
        links = handler.handle(event)

        # then
        self.generator.encode.assert_called_with({
            TITLE: 'my great article',
            ARTICLE_ID: '123',
            USER_ID: 321,
            OPERATION: SAVE_ARTICLE
        })
        self.assertEqual('Click to star article', links['links']['123'][0]['action'])
        self.assertEqual(1, len(links['links']))
        self.assertEqual(1, len(links['links']['123']))
