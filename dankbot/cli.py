from __future__ import print_function

import os
from datetime import datetime as dt
from configparser import ConfigParser

import praw
import MySQLdb as mdb
from slacker import Slacker

MAX_MEMES = 1


class DankBot(object):
    '''
    Bot for posting dank memes from reddit to slack
    '''
    def __init__(self, slack_token, channel, subreddits, database, username, password):
        self.slack_token = slack_token
        self.channel = channel
        self.subreddits = subreddits
        self.database = database
        self.username = username
        self.password = password

    def go(self):
        # Check for most recent dank memes
        memes = self.get_memes()

        # Filter out any known dank memes
        filtered_memes = [m for m in memes if not self.in_collection(m)]

        # Cut down to the max memes
        chopped_memes = filtered_memes[:MAX_MEMES]

        # If any are left, post to slack
        self.post_to_slack(chopped_memes)

    def get_memes(self):
        '''
        Collect top memes from r/dankmemes
        '''

        # Build the user_agent, this is important to conform to Reddit's rules
        user_agent = 'linux:dankscraper:0.0.2 (by /u/IHKAS1984)'

        # Create connection object
        r = praw.Reddit(user_agent=user_agent)

        memes = list()

        func = r.get_subreddit

        for sub in self.subreddits:
            memes += [Meme(link.url, sub) for link in func(sub).get_hot()]

        return memes

    def in_collection(self, meme):
        '''
        Checks to see if the supplied meme is already in the collection of known
        memes
        '''
        query = "SELECT * FROM memes WHERE links = '{0}'".format(meme.link)

        con = mdb.connect(
                'localhost', self.username, self.password, self.database)

        with con:
            cur = con.cursor()
            resp = cur.execute(query)

        return True if resp else False

    def add_to_collection(self, meme):
        '''
        Adds a meme to the collection
        '''
        query = """INSERT INTO memes 
                   (links, sources, datecreated) 
                   VALUES
                   ('{0}', '{1}', '{2}')
                """.format(meme.link, meme.source, str(dt.now()))

        con = mdb.connect(
                'localhost', self.username, self.password, self.database)

        with con:
            cur = con.cursor()
            cur.execute(query)

    def post_to_slack(self, memes):
        '''
        Post the memes to slack
        '''
        slack = Slacker(self.slack_token)
        for meme in memes:
            resp = slack.chat.post_message(self.channel, meme.link, as_user=True)

            if resp.successful:
                self.add_to_collection(meme)


class Meme(object):
    """
    Model for meme objects
    """
    def __init__(self, link, source):
        self.link = link
        self.source = source


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

    subreddits = [s.strip(',') for s in config['reddit']['subreddits'].split()]

    DankBot(
        slack_token=token,
        channel=channel,
        subreddits=subreddits,
        database=database,
        username=username,
        password=password
    ).go()


if __name__ == "__main__":
    main()
