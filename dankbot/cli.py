from __future__ import print_function

import logging
from os import path
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler

from dankbot.dankbot import DankBot

logger = logging.getLogger("Dankbot Rotating Log")
logger.setLevel(logging.INFO)


def create_rotating_log(dir_path):
    """
    Creates a rotating log

    :param dir_path: String, path to current directory
    """
    # Set the log path to the log directory
    log_path = path.join(dir_path, 'logs', 'dankbot.log')
 
    # add a rotating handler
    handler = RotatingFileHandler(log_path, maxBytes=1000000,
                                  backupCount=5)
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

    DankBot(config).find_and_post_memes()


if __name__ == "__main__":
    main()
