#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Loads config file
"""

import os
import yaml

def load_config():
    config_file = '../config.yml'
    global config
    if os.path.isfile(config_file):
        with open(config_file) as f:
            config = yaml.load(f)

    else:
        print 'no config found'
        exit(1)

def get(key):
    global config
    if config is None:
        load_config()
    return config[key]

