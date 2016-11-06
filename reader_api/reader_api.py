#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler import execute_action, generate_links
import config

def handle(event):
    if config.ACTION_PARAM in event:
        # execute API action
        return execute_action.handle(event)
    else:
        # generate API action links
        return generate_links.handle(event)
