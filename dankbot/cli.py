import os
import sys
import logging
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler

import appdirs

from dankbot.dankbot import DankBot
from dankbot import APPNAME, APPAUTHOR

DEFAULT_CONFIG = 'dankbot.ini'


def load_config():
    config = ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), DEFAULT_CONFIG)
    config.read(config_path)

    return config


def configure_logger(log_config):
    """
    Creates a rotating log

    :param config_dir_path: String, path to current directory
    """
    # Create Logger object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Formatting
    formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')

    # Set up STDOUT handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    # Log to file if set in config
    if log_config.getboolean('log_to_file'):
        log_dir = log_config['directory'] or appdirs.user_log_dir(APPNAME, APPAUTHOR)
        log_path = os.path.join(log_dir, log_config['file_name'])

        # Create the logging directory if it doesn't exist
        if not os.path.exists(log_dir):  # pragma: no cover
            os.makedirs(log_dir)

        # Set up file logging with rotating file handler
        backups = log_config.getint('backups')
        max_bytes = log_config.getint('max_bytes')
        rotate_fh = RotatingFileHandler(
            log_path, backupCount=backups, maxBytes=max_bytes
        )
        rotate_fh.setLevel(logging.DEBUG)
        rotate_fh.setFormatter(formatter)

        logger.addHandler(rotate_fh)
    else:  # pragma: no cover
        log_path = None

    return logger, log_path


def main():
    # Load the configuration options
    config = load_config()

    # Load the logger
    logger, log_path = configure_logger(config['dankbot'])

    logger.info("Dankbot run starting")
    logger.info("Dankbot configuration loaded")
    logger.info("Logging to: {0}".format(log_path))  # pylint: disable=W1202

    try:
        DankBot(config, logger).find_and_post_memes()
    except Exception:  # pylint: disable=W0703
        logger.exception("Caught exception:")
