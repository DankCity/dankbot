import logging
from unittest import mock
from unittest.mock import patch, call
from configparser import ConfigParser

import pytest

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

IMGUR_CLIENT_ID = "mock imgur client id"
IMGUR_CLIENT_SECRET = "mock imgur secret"

DANK_MEME_URL = "http://dank.meme.url"
IMGUR_MEME_URL = "http://imgur.com/mockhash"


class MockMeme(object):
    def __init__(self, over_18, url):
        self.over_18 = False
        self.url = url


@pytest.fixture(scope="function")
def slack():
    with patch('dankbot.dankbot.Slacker') as slack:
        slack.return_value = slack
        slack.chat = slack
        slack.post_message.return_value = slack
        slack.successful = True

        yield slack


@pytest.fixture(scope="function")
def praw(dank_meme):
    with patch('dankbot.dankbot.praw') as praw:
        praw.Reddit.return_value = praw
        praw.get_subreddit.return_value = praw
        praw.get_hot.return_value = [dank_meme, ]

        yield praw


@pytest.fixture(scope="function")
def dank_meme():
    return MockMeme(False, DANK_MEME_URL)


@pytest.fixture(scope="function")
def imgur_meme():
    return MockMeme(False, IMGUR_MEME_URL)


@pytest.fixture(scope="function")
def config():
    ''' Returns a mock configuration object
    '''
    config_dict = {
        'slack': {
            'channel': MOCK_CHANNEL,
            'token': MOCK_TOKEN,
        },
        'mysql': {
            'database': MOCK_DB,
            'username': MOCK_UN,
            'password': MOCK_PW,
        },
        'misc': {
            'include_nsfw': INCLUDE_NSFW,
            'max_memes': MAX_MEMES
        },
        'reddit': {
            'subreddits': SUBREDDITS
        },
        'imgur': {
            'client_id': IMGUR_CLIENT_ID,
            'client_secret': IMGUR_CLIENT_SECRET
        }
    }

    config_ = ConfigParser()
    config_.read_dict(config_dict)

    return config_


@pytest.fixture(scope="function")
def logger():
    ''' Returns a mock logger
    '''
    return mock.create_autospec(logging.Logger)


def test___init__(config, logger):
    dankbot = DankBot(config, logger)

    assert dankbot.slack_token == MOCK_TOKEN
    assert dankbot.slack_channel == MOCK_CHANNEL
    assert dankbot.database == MOCK_DB
    assert dankbot.username == MOCK_UN
    assert dankbot.password == MOCK_PW
    assert dankbot.include_nsfw == INCLUDE_NSFW
    assert dankbot.max_memes == MAX_MEMES
    assert SUB_1 in dankbot.subreddits
    assert SUB_2 in dankbot.subreddits
    assert SUB_3 in dankbot.subreddits
    assert dankbot.logger == logger

    assert ImgurMeme.client_id == IMGUR_CLIENT_ID
    assert ImgurMeme.client_secret == IMGUR_CLIENT_SECRET


@patch.object(DankBot, 'add_to_collection')
@patch.object(DankBot, 'in_collection')
def test_find_and_post(ic, atc, praw, slack, config, logger):
    ic.return_value = False

    dankbot = DankBot(config, logger)
    dankbot.subreddits = dankbot.subreddits[:1]

    resp = dankbot.find_and_post_memes()

    assert slack.post_message.called
    assert resp is True
    assert atc.called

    message = "from {0}: {1}".format(SUB_1, DANK_MEME_URL)
    assert slack.post_message.call_args == call(MOCK_CHANNEL, message, as_user=True)


@patch.object(DankBot, 'in_collection')
def test_find_and_post_in_collection(ic, praw, config, logger):
    ic.return_value = True

    dankbot = DankBot(config, logger)
    dankbot.subreddits = dankbot.subreddits[:1]

    resp = dankbot.find_and_post_memes()

    assert resp is False


@patch.object(DankBot, 'in_collection')
def test_no_nsfw_and_18plus(ic, praw, config, logger):
    ic.return_value = False
    praw.get_hot.return_value[0].over_18 = True

    dankbot = DankBot(config, logger)
    dankbot.subreddits = dankbot.subreddits[:1]

    resp = dankbot.find_and_post_memes()

    assert resp is False


@patch.object(DankBot, 'add_to_collection')
@patch.object(DankBot, 'in_collection')
def test_yes_nsfw_and_18plus(ic, atc, slack, praw, config, logger):
    ic.return_value = False
    praw.get_hot.return_value[0].over_18 = True

    dankbot = DankBot(config, logger)
    dankbot.include_nsfw = True
    dankbot.subreddits = dankbot.subreddits[:1]

    resp = dankbot.find_and_post_memes()

    assert slack.post_message.called
    assert resp is True
    assert atc.called

    message = "from {0}: {1}".format(SUB_1, DANK_MEME_URL)
    assert slack.post_message.call_args == call(MOCK_CHANNEL, message, as_user=True)


@patch('dankbot.dankbot.praw')
@patch('dankbot.memes.ImgurClient')
@patch.object(DankBot, 'add_to_collection')
@patch.object(DankBot, 'in_collection')
def test_post_imgur_meme(ic, atc, imgur, praw, slack, config, logger, imgur_meme):
    ic.return_value = False
    imgur.return_value = Exception("Preventing connection")
    praw.Reddit.return_value = praw
    praw.get_subreddit.return_value = praw
    praw.get_hot.return_value = [imgur_meme, ]

    dankbot = DankBot(config, logger)
    dankbot.subreddits = dankbot.subreddits[:1]

    resp = dankbot.find_and_post_memes()

    assert slack.post_message.called
    assert resp is True
    assert atc.called

    message = "from {0}: {1}".format(SUB_1, IMGUR_MEME_URL)
    assert slack.post_message.call_args == call(MOCK_CHANNEL, message, as_user=True)
