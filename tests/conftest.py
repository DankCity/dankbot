import pytest
from unittest.mock import patch

from tests import RedditMeme, test_vars as tv
from dankbot.memes import ImgurMeme, DankMeme, Meme


@pytest.fixture
def meme():
    return Meme(RedditMeme())


@pytest.fixture
def dank_meme():
    return DankMeme(RedditMeme())


@pytest.fixture
def imgur_direct_meme():
    ImgurMeme.set_credentials(tv['CLIENT_ID'], tv['CLIENT_SECRET'])
    return ImgurMeme(RedditMeme(url=tv['TEST_DIRECT_LINK']))


@pytest.fixture
def imgur_image_meme():
    ImgurMeme.set_credentials(tv['CLIENT_ID'], tv['CLIENT_SECRET'])
    return ImgurMeme(RedditMeme(url=tv['TEST_IMAGE_LINK']))


@pytest.fixture
def imgur_image_meme_2():
    ImgurMeme.set_credentials(tv['CLIENT_ID'], tv['CLIENT_SECRET'])
    return ImgurMeme(RedditMeme(sub=tv['TEST_SUBREDDIT_4'],
                                url=tv['TEST_IMAGE_LINK_1']))


@pytest.fixture
def imgur_album_meme_1():
    ImgurMeme.set_credentials(tv['CLIENT_ID'], tv['CLIENT_SECRET'])
    return ImgurMeme(RedditMeme(url=tv['TEST_ALBUM_LINK_1']))


@pytest.fixture
def imgur_album_meme_2():
    ImgurMeme.set_credentials(tv['CLIENT_ID'], tv['CLIENT_SECRET'])
    return ImgurMeme(RedditMeme(sub=tv['TEST_SUBREDDIT_2'],
                                url=tv['TEST_ALBUM_LINK_2']))


@pytest.fixture
def imgur_gallery_meme_1():
    ImgurMeme.set_credentials(tv['CLIENT_ID'], tv['CLIENT_SECRET'])
    return ImgurMeme(RedditMeme(sub=tv['TEST_SUBREDDIT_3'],
                                url=tv['TEST_GALLERY_LINK_1']))


@pytest.fixture
def client():
    with patch("dankbot.memes.ImgurClient") as client:
        client.return_value = client
        client.get_image.return_value = client
        client.gallery_item.return_value = client
        client.get_album.return_value = client

        yield client
