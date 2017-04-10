#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler import execute_action, generate_links

def handle(event):
    if is_http(event):
        # execute API action
        return execute_action.handle(event)
    else:
        # generate API action links
        return generate_links.handle(event)


def is_http(event):
    return 'httpMethod' in event
