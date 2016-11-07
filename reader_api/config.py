#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Loads config file
"""

import os
import yaml

ACTION_PARAM = 'action'
# TODO fix
#SELF_URL = 'https://api.keendly.com/reader?action='
SELF_URL = 'http://localhost:5000/execute?{}='.format(ACTION_PARAM)

config = None

def get(key):
    global config
    if config is None:
        config = load_config()
    return config[key]

def load_config():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        print f
        # do something

    config_file = '../config.yml'
    if os.path.isfile(config_file):
        with open(config_file) as f:
            return yaml.load(f)

    else:
        print 'no config found'
        exit(1)


