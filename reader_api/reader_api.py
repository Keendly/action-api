#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler import execute_action, generate_links

import time

def handle(event):
    if is_http(event):
        # execute API action
        return execute_action.handle(event)
    else:
        # generate API action links
        ret =  generate_links.handle(event)
        print ret
        return ret


def is_http(event):
    return 'httpMethod' in event
