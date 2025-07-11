#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
"""

import os
import logging
import traceback
from logging.config import dictConfig
from src.core.application_constants import LOGGING_LEVEL, EMAIL_SECRET, EMAIL_ADDRESS, EMAIL_TO_ADDRESS

try:
    from pythonjsonlogger import jsonlogger

    JSON_LOGGING_AVAILABLE = True
except ImportError:
    JSON_LOGGING_AVAILABLE = False

DEFAULT_LOG_FILENAME = 'app.log'
DEFAULT_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
DEFAULT_BACKUP_COUNT = 5
SUPPRESSED_LOGGERS = ['seleniumwire', 'imapclient', 'imapclient.imaplib', 'urllib3', 'WDM',
                      'undetected_chromedriver', 'selenium', 'faker.factory', 'hpack']


def get_log_config(log_dir, filename=DEFAULT_LOG_FILENAME, use_json=False, enable_email=False):
    """Return the logging config dictionary."""
    formatter_type = 'json' if use_json and JSON_LOGGING_AVAILABLE else 'default'

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, filename),
                'maxBytes': DEFAULT_MAX_BYTES,
                'backupCount': DEFAULT_BACKUP_COUNT,
                'formatter': formatter_type,
            },
            'stream': {
                'class': 'logging.StreamHandler',
                'formatter': formatter_type,
            },
        },
        'root': {
            'level': LOGGING_LEVEL,
            'handlers': ['file', 'stream']
        },
    }

    if use_json and JSON_LOGGING_AVAILABLE:
        config['formatters']['json'] = {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }

    if enable_email:
        config['handlers']['email'] = {
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': ('smtp.gmail.com', 587),
            'fromaddr': EMAIL_ADDRESS,
            'toaddrs': [EMAIL_TO_ADDRESS],
            'subject': 'Critical Error in Application',
            'credentials': (EMAIL_ADDRESS, EMAIL_SECRET),
            'secure': (),
            'level': 'CRITICAL',
            'formatter': 'default',
        }
        config['root']['handlers'].append('email')

    return config


def suppress_noise_loggers(logger_names):
    for name in logger_names:
        logging.getLogger(name).setLevel(logging.ERROR)


def init_logging(save_location='logs', use_json=False, enable_email=False):
    """Setup application-wide logging."""
    try:
        log_dir = os.path.join(save_location)
        os.makedirs(log_dir, exist_ok=True)

        logging.root.handlers.clear()

        config = get_log_config(
            log_dir=log_dir,
            use_json=use_json,
            enable_email=enable_email
        )
        dictConfig(config)
        suppress_noise_loggers(SUPPRESSED_LOGGERS)

        logging.getLogger(__name__).info("Logging initialized successfully.")

    except Exception as e:
        print("Logging setup failed:")
        print(f"{type(e).__name__}: {e}")
        traceback.print_exc()
