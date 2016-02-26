from __future__ import print_function

import os
from configparser import ConfigParser

from dankbot.dankbot import DankBot


def main():
    # Load the configuration options
    config = ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), u'dankbot.ini')
    config.read(config_path)

    token = config['slack']['token']
    channel = config['slack']['channel']
    database = config['mysql']['database']
    username = config['mysql']['username']
    password = config['mysql']['password']
    include_nsfw = config.getboolean('misc', 'include_nsfw')
    max_memes = config.getint('misc', 'max_memes')

    subreddits = [s.strip(',') for s in config['reddit']['subreddits'].split()]

    DankBot(
        slack_token=token,
        channel=channel,
        subreddits=subreddits,
        database=database,
        username=username,
        password=password,
        include_nsfw=include_nsfw,
        max_memes=max_memes
    ).go()


if __name__ == "__main__":
    main()
