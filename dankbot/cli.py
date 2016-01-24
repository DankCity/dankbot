from __future__ import print_function

import os
from configparser import ConfigParser

import praw
from slacker import Slacker


class DankBot(object):
    '''
    Bot for posting dank memes from reddit to slack
    '''
    def __init__(self, slack_token, channel, subreddits):
        self.slack_token = slack_token
        self.channel = channel
        self.subreddits = subreddits

    def go(self):
        # Check for most recent dank memes
        memes = self.get_memes()

        # Filter out any known dank memes
        filtered_memes = [m for m in memes if not self.in_collection(m)]

        # If any are left, post to slack
        self.post_to_slack(filtered_memes)

    def get_memes(self):
        '''
        Collect top memes from r/dankmemes
        '''

        # Build the user_agent, this is important to conform to Reddit's rules
        user_agent = 'linux:dankscraper:0.0.2 (by /u/IHKAS1984)'

        # Create connection object
        r = praw.Reddit(user_agent=user_agent)

        memes = list()

        for subreddit in self.subreddits:
            memes += [h.url for h in r.get_subreddit(subreddit).get_hot()]

        return memes

    def in_collection(self, meme):
        '''
        Checks to see if the supplied meme is already in the collection of known
        memes
        '''
        pass

    def add_to_collection(self, meme):
        '''
        Adds a meme to the collection
        '''
        pass

    def post_to_slack(self, memes):
        '''
        Post the memes to slack
        '''
        slack = Slacker(self.slack_token)
        for meme in memes:
            resp = slack.chat.post_message(self.channel, meme, as_user=True)
            break

            '''
            if resp.successful:
                self.add_to_collection(meme)
            '''


def main():
    # Load the configuration options
    config = ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), u'dankbot.ini')
    config.read(config_path)

    token = config['slack']['token']
    channel = config['slack']['channel']
    subreddits = [s.strip(',') for s in config['reddit']['subreddits'].split()]

    DankBot(slack_token=token, channel=channel, subreddits=subreddits).go()


if __name__ == "__main__":
    main()
