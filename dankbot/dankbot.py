from __future__ import print_function

import random
from datetime import datetime as dt

import praw
import MySQLdb as mdb
from slacker import Slacker

from dankbot.memes import ImgurMeme, DankMeme


class DankBot(object):
    '''
    Bot for posting dank memes from reddit to slack
    '''
    def __init__(self, config):
        self.slack_token = config['slack']['token']
        self.channel = config['slack']['channel']

        self.database = config['mysql']['database']
        self.username = config['mysql']['username']
        self.password = config['mysql']['password']

        self.include_nsfw = config.getboolean('misc', 'include_nsfw')
        self.max_memes = config.getint('misc', 'max_memes')

        self.subreddits = [s.strip(',') for s in config['reddit']['subreddits'].split()]

        # Get and set Imgur API credentials
        client_id = config['imgur']['client_id']
        client_secret = config['imgur']['client_secret']

        ImgurMeme.set_credentials(client_id=client_id, client_secret=client_secret)

    def go(self):
        # Check for most recent dank memes
        memes = self.get_memes()

        # Filter out any known dank memes
        filtered_memes = [m for m in memes if not self.in_collection(m)]

        # Shuffle memes
        random.shuffle(filtered_memes)

        # Cut down to the max memes
        pared_memes = filtered_memes[:self.max_memes]

        # Bale here if nothing is left
        if not pared_memes:
            return False

        # If any memes are Imgur galleries, get more information
        for meme in [meme for meme in pared_memes if isinstance(meme, ImgurMeme)]:
            try:
                meme.digest()
            except:
                raise

        # Post to slack
        return self.post_to_slack(pared_memes)

    def get_memes(self):
        '''
        Collect top memes from r/dankmemes
        '''

        # Build the user_agent, this is important to conform to Reddit's rules
        user_agent = 'linux:dankscraper:0.0.3 (by /u/IHKAS1984)'

        # Create connection object
        r = praw.Reddit(user_agent=user_agent)

        memes = list()

        # Get list of memes, filtering out NSFW entries
        for sub in self.subreddits:
            for meme in r.get_subreddit(sub).get_hot():
                if meme.over_18 and not self.include_nsfw:
                    continue

                if "imgur.com/" in meme.url:
                    memes.append(ImgurMeme(meme.url, sub))
                else:
                    memes.append(DankMeme(meme.url, sub))

        return memes

    @staticmethod
    def _is_imgur_album(link):
        """
        Returns True if link is an Imgur front page album
        """
        return True if "imgur.com/a/" in link else False

    @staticmethod
    def _is_imgur_gallery(link):
        """
        Returns True if link is an Imgur user album
        """
        return True if "imgur.com/gallery/" in link else False

    @staticmethod
    def _is_imgur_image(link):
        """
        Returns True if link is an Imgur image
        """
        return True if "imgur.com/" in link else False

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

        with con, con.cursor() as cur:
            cur.execute(query)

        return

    def post_to_slack(self, memes):
        '''
        Post the memes to slack
        '''
        ret_status = False

        slack = Slacker(self.slack_token)
        for meme in memes:

            message = meme.format_for_slack()
            resp = slack.chat.post_message(self.channel, message, as_user=True)

            if resp.successful:
                self.add_to_collection(meme)
                ret_status = True

        return ret_status
