import praw
from slacker import Slacker


def get_memes():
    '''
    Collect top memes from r/dankmemes
    '''

    # Build the user_agent, this is important to conform to Reddit's rules
    user_agent = 'linux:dankscraper:0.0.1 (by /u/IHKAS1984)'

    # Create connection object
    r = praw.Reddit(user_agent=user_agent)

    return [h.url for h in r.get_subreddit('dankmemes').get_hot()]


def post_to_slack(memes):
    '''
    Post the memes to slack
    '''
    slack = Slacker('redacted')
    for meme in memes:
        slack.chat.post_message('#random', meme, as_user=True)
        break


def filter_my_memes(memes):
    '''
    '''
    pass


def main():
    # Check for most recent dank memes
    memes = get_memes()

    # Filter out any known dank memes
    filtered_memes = filter_my_memes(memes)

    # If any are left, post to slack
    post_to_slack(memes)


if __name__ == "__main__":
    pass
