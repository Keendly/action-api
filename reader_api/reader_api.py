#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler import execute_action_handler, generate_tokens_handler

def handle(event):
    if 'action' in event:
        # execute API action
        return execute_action_handler.handle(event)
    else:
        # generate API action links
        return generate_tokens_handler.handle(event)
