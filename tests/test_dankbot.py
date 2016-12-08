import time
import logging
from unittest import mock
from unittest.mock import patch
from configparser import ConfigParser

import pytest

from tests import test_vars as tv, RedditMeme
from dankbot.db import DB
from dankbot.dankbot import DankBot
from dankbot.memes import ImgurMeme

MOCK_TOKEN = "mock_token"
MOCK_CHANNEL = "mock_slack_channel"

MOCK_DB = "mock_db"
MOCK_UN = "mock_username"
MOCK_PW = "mock_password"

INCLUDE_NSFW = False
MAX_MEMES = 5

SUB_1 = "dankmemes"
SUB_2 = "fishpost"
SUB_3 = "memes"
SUBREDDITS = ", ".join([SUB_1, SUB_2, SUB_3])

CLIENT_ID = "mock imgur client id"
CLIENT_SECRET = "mock imgur secret"

DANK_MEME_URL = "http://dank.meme.url"
IMGUR_MEME_URL = "http://imgur.com/mockhash"


@pytest.fixture(scope="function")
def slack():
    with patch('dankbot.dankbot.Slacker') as slack:
        slack.return_value = slack
        slack.chat = slack
        slack.post_message.return_value = slack
        slack.successful = True

        yield slack


@pytest.fixture(scope="function")
def praw():
    with patch('dankbot.dankbot.praw') as praw:
        praw.Reddit.return_value = praw
        praw.get_subreddit.return_value = praw
        praw.get_hot.return_value = [RedditMeme(), ]

        yield praw


@pytest.fixture(scope="function")
def praw_nsfw():
    with patch('dankbot.dankbot.praw') as praw:
        praw.Reddit.return_value = praw
        praw.get_subreddit.return_value = praw
        praw.get_hot.return_value = [RedditMeme(over_18=True), ]

        yield praw


@pytest.fixture(scope="function")
def praw_imgur():
    with patch('dankbot.dankbot.praw') as praw:
        praw.Reddit.return_value = praw
        praw.get_subreddit.return_value = praw
        praw.get_hot.return_value = [RedditMeme(url=tv['TEST_IMAGE_LINK_1']), ]

        yield praw


@pytest.fixture(scope="function")
def config():
    ''' Returns a mock configuration object
    '''
    config_dict = {
        'dankbot': {
            'log_to_file': True,
            'directory': '',
            'file_name': 'dankbot.log',
            'backups': 5,
            'max_bytes': 1000000
        },
        'imgur': {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET},
        'misc': {'include_nsfw': INCLUDE_NSFW, 'max_memes': MAX_MEMES},
        'reddit': {'subreddits': SUBREDDITS},
        'slack': {'channel': MOCK_CHANNEL, 'token': MOCK_TOKEN}
    }

    config_ = ConfigParser()
    config_.read_dict(config_dict)

    return config_


@pytest.fixture(scope="function")
def logger():
    ''' Returns a mock logger
    '''
    return mock.create_autospec(logging.Logger)


@pytest.fixture
def dankbot(config, logger, praw):
    with patch('dankbot.db.join', return_value=":memory:"):
        yield DankBot(config, logger)


@pytest.fixture
def dankbot_nsfw(config, logger, praw_nsfw):
    with patch('dankbot.db.join', return_value=":memory:"):
        yield DankBot(config, logger)


@pytest.fixture
def dankbot_imgur(config, logger, praw_imgur):
    with patch('dankbot.db.join', return_value=":memory:"):
        yield DankBot(config, logger)


@patch('dankbot.db.join', return_value=":memory:")
def test___init__(_, config, logger):
    dankbot = DankBot(config, logger)

    assert dankbot.slack_token == MOCK_TOKEN
    assert dankbot.slack_channel == MOCK_CHANNEL
    assert dankbot.include_nsfw == INCLUDE_NSFW
    assert dankbot.max_memes == MAX_MEMES
    assert SUB_1 in dankbot.subreddits
    assert SUB_2 in dankbot.subreddits
    assert SUB_3 in dankbot.subreddits
    assert dankbot.logger == logger

    assert isinstance(dankbot.db, DB)
    assert dankbot.db.db_path == ":memory:"

    assert ImgurMeme.client_id == CLIENT_ID
    assert ImgurMeme.client_secret == CLIENT_SECRET


def test_find_and_post(dankbot, slack):
    dankbot.subreddits = dankbot.subreddits[:1]

    resp = dankbot.find_and_post_memes()

    assert slack.post_message.called
    assert resp is True

    message = "from {0}: {1}".format(tv['TEST_SUBREDDIT'], tv['TEST_LINK'])
    assert slack.post_message.call_args[0][0] == MOCK_CHANNEL
    assert slack.post_message.call_args[0][1] == message


def test_find_and_post_in_collection(dankbot, dank_meme, slack):
    dankbot.subreddits = dankbot.subreddits[:1]
    dankbot.db.add_to_collection(dank_meme)

    resp = dankbot.find_and_post_memes()

    assert resp is False
    assert not slack.post_message.called


def test_no_nsfw_and_18plus(dankbot_nsfw, slack):
    dankbot_nsfw.subreddits = dankbot_nsfw.subreddits[:1]

    resp = dankbot_nsfw.find_and_post_memes()

    assert resp is False
    assert not slack.post_message.called


def test_yes_nsfw_and_18plus(dankbot_nsfw, slack):
    dankbot_nsfw.include_nsfw = True
    dankbot_nsfw.subreddits = dankbot_nsfw.subreddits[:1]

    resp = dankbot_nsfw.find_and_post_memes()

    assert slack.post_message.called
    assert resp is True

    message = "from {0}: {1}".format(tv['TEST_SUBREDDIT'], tv['TEST_LINK'])
    assert slack.post_message.call_args[0][0] == MOCK_CHANNEL
    assert slack.post_message.call_args[0][1] == message


@patch('dankbot.memes.ImgurClient')
def test_post_imgur_meme(client, dankbot_imgur, slack):
    client.return_value = Exception("Preventing connection")

    dankbot_imgur.subreddits = dankbot_imgur.subreddits[:1]

    resp = dankbot_imgur.find_and_post_memes()

    assert slack.post_message.called
    assert resp is True

    message = "from {0}: {1}".format(tv['TEST_SUBREDDIT'], tv['TEST_IMAGE_LINK_1'])
    assert slack.post_message.call_args[0][0] == MOCK_CHANNEL
    assert slack.post_message.call_args[0][1] == message


def test_last_seen_update(dankbot, slack, dank_meme):
    dankbot.db.add_to_collection(dank_meme)
    query = "SELECT last_seen from memes where reddit_id=:reddit_id"
    first_meme_time = dankbot.db._query(query, {'reddit_id': dank_meme.reddit_id})
    time.sleep(2)
    dankbot.subreddits = dankbot.subreddits[:1]

    resp = dankbot.find_and_post_memes()
    second_meme_time = dankbot.db._query(query, {'reddit_id': dank_meme.reddit_id})

    assert resp is False
    assert not slack.post_message.called

    assert first_meme_time != second_meme_time
