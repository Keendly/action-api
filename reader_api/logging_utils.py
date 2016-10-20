#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pythonjsonlogger import jsonlogger

def get_logger(name, level=logging.DEBUG):
    log_format = lambda x: ['%({0:s})'.format(i) for i in x]
    custom_format = ' '.join(log_format(supported_keys))
    logger = logging.getLogger(name)
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(custom_format)
    logHandler.setFormatter(formatter)
    logHandler.setLevel(level)
    logger.addHandler(logHandler)
    logger.setLevel(level)
    logging.basicConfig(level=level)
    return logger

supported_keys = [
    'asctime',
    'created',
    'filename',
    'funcName',
    'levelname',
    'module',
    'message',
    'threadName'
]


