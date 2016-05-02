from __future__ import print_function

import logging
import logging.config
from os import path
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler

from dankbot.dankbot import DankBot


logging.config.fileConfig('log.conf', disable_existing_loggers=0)
logger = logging.getLogger('dankbot')
'''
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s %(asctime)s] %(message)s'
)
logger = logging.getLogger(__name__)
'''
logger.info("TESTING")
import sys
sys.exit()


def create_rotating_log(dir_path):
    """
    Creates a rotating log

    :param dir_path: String, path to current directory
    """
    # Set the log path to the log directory
    log_path = path.join(dir_path, 'logs', 'dankbot.log')

    # Add a rotating handler
    handler = RotatingFileHandler(
        log_path, 
        backupCount=5,
        maxBytes=1000000
    )
    formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def main():
    # Get the current filepath
    dir_path = path.dirname(__file__)

    # Setup the logger
    create_rotating_log(dir_path)

    logger.info("Dankbot run starting")

    # Load the configuration options
    logger.info("Loading Dankbot Configuration")
    config = ConfigParser()
    config_path = path.join(dir_path, u'dankbot.ini')
    config.read(config_path)

    try:
        DankBot(config).find_and_post_memes()
    except Exception:
        logger.exception("Caught exception:")


if __name__ == "__main__":
    main()
