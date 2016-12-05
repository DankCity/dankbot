import os
import sys
import logging
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler

import appdirs

from dankbot.dankbot import DankBot
from dankbot import APPNAME, APPAUTHOR

LOG_DIR = appdirs.user_log_dir(APPNAME, APPAUTHOR)
LOG_FILE = os.path.join(LOG_DIR, "dankbot.log")


def configure_logger():
    """
    Creates a rotating log

    :param dir_path: String, path to current directory
    """
    # Create the logging directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Formatting
    formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')

    # Set up STDOUT handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    # Set up file logging with rotating file handler
    rotate_fh = RotatingFileHandler(LOG_FILE, backupCount=5, maxBytes=1000000)
    rotate_fh.setLevel(logging.DEBUG)
    rotate_fh.setFormatter(formatter)

    # Create Logger object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stdout_handler)
    logger.addHandler(rotate_fh)

    return logger


def main():
    # Setup the logger
    logger = configure_logger()

    logger.info("Dankbot run starting")
    logger.info("Logging to: {0}".format(LOG_FILE))

    # Load the configuration options
    logger.info("Loading Dankbot Configuration")
    config = ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), u'dankbot.ini')
    config.read(config_path)

    try:
        DankBot(config, logger).find_and_post_memes()
    except Exception:  # pylint: disable=W0703
        logger.exception("Caught exception:")
