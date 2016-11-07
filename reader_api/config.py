#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Loads config file
"""

import os
import yaml

ACTION_PARAM = 'action'
# TODO fix
#SELF_URL = 'https://api.keendly.com/reader?{}='
SELF_URL = 'https://amv54jkwba.execute-api.eu-west-1.amazonaws.com/prod?{}='.format(ACTION_PARAM)

config = None

def get(key):
    global config
    if config is None:
        config = load_config()
    return config[key]

def load_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file = '{}/../config.yml'.format(dir_path)
    if os.path.isfile(config_file):
        with open(config_file) as f:
            return yaml.load(f)

    else:
        print 'no config found'
        exit(1)


