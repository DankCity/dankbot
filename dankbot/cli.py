from __future__ import print_function

import os
from configparser import ConfigParser

from dankbot.dankbot import DankBot


def main():
    # Load the configuration options
    config = ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), u'dankbot.ini')
    config.read(config_path)

    DankBot(config).find_memes()


if __name__ == "__main__":
    main()
