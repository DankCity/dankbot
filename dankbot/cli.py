from __future__ import print_function

import sys
import logging
from os import path
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler

from dankbot.dankbot import DankBot

LOG_FILE = "/var/log/dankbot/dankbot.log"


def configure_logger():
    """
    Creates a rotating log

    :param dir_path: String, path to current directory
    """
    # Formatting
    formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')

    # Set up STDOUT handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)

    # Set up file logging with rotating file handler
    rfh = RotatingFileHandler(LOG_FILE, backupCount=5, maxBytes=1000000)
    rfh.setLevel(logging.DEBUG)
    rfh.setFormatter(formatter)

    # Create Logger object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(rfh)

    return logger


def main():
    # Setup the logger
    logger = configure_logger()

    logger.info("Dankbot run starting")

    # Load the configuration options
    logger.info("Loading Dankbot Configuration")
    config = ConfigParser()
    config_path = path.join(path.dirname(__file__), u'dankbot.ini')
    config.read(config_path)

    try:
        DankBot(config, logger).find_and_post_memes()
    except Exception:
        logger.exception("Caught exception:")


if __name__ == "__main__":
    main()
