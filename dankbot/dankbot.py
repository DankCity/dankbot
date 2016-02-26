from __future__ import print_function

import random
from datetime import datetime as dt

import praw
import MySQLdb as mdb
from slacker import Slacker

from dankbot.meme import ImgurMeme, DankMeme

MAX_MEMES = 3


class DankBot(object):
    '''
    Bot for posting dank memes from reddit to slack
    '''
    def __init__(self, slack_token, channel, subreddits, database, username,
                 password, include_nsfw, max_memes=MAX_MEMES):
        self.slack_token = slack_token
        self.channel = channel
        self.subreddits = subreddits
        self.database = database
        self.username = username
        self.password = password
        self.include_nsfw = include_nsfw
        self.max_memes = max_memes

    def go(self):
        # Check for most recent dank memes
        memes = self.get_memes()

        # Filter out any known dank memes
        filtered_memes = [m for m in memes if not self.in_collection(m)]

        # Shuffle memes
        random.shuffle(filtered_memes)

        # Cut down to the max memes
        chopped_memes = filtered_memes[:self.max_memes]

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

        # Get list of memes, filtering out NSFW entries
        for sub in self.subreddits:
            for meme in r.get_subreddit(sub).get_hot():
                if meme.over_18 and not self.include_nsfw:
                    continue

                if self._is_imgur_gallery(meme.url):
                    memes.append(ImgurMeme(meme.url, sub))
                else:
                    memes.append(DankMeme(meme.url, sub))

        return memes

    @staticmethod
    def _is_imgur_gallery(link):
        """
        Returns True if link leads to imgur
        """
        image_types = ["jpg", "png", "gif", "gifv"]
        if "imgur.com" not in link:
            return False
        elif any([img_type in link.lower() for img_type in image_types]):
            return False
        else:
            return True

    def in_collection(self, meme):
        '''
        Checks to see if the supplied meme is already in the collection of known
        memes
        '''
        query = "SELECT * FROM memes WHERE links = '{0}'".format(meme.link)

        con = mdb.connect(
            'localhost', self.username, self.password, self.database)

        with con, con.cursor() as cur:
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

            message = meme.format_for_slack()
            resp = slack.chat.post_message(self.channel, message, as_user=True)

            if resp.successful:
                self.add_to_collection(meme)
