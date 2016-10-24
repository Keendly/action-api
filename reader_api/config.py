#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Loads config file
"""

import os
import yaml

config = None

def get(key):
    global config
    if config is None:
        config = load_config()
    return config[key]

def load_config():
    config_file = '../config.yml'
    if os.path.isfile(config_file):
        with open(config_file) as f:
            return yaml.load(f)

    else:
        print 'no config found'
        exit(1)

