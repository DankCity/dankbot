import pytest
from unittest.mock import patch

from dankbot.memes import ImgurMeme, DankMeme, Meme, UndigestedError

TEST_LINK = "test meme link"
TEST_SUBREDDIT = "test subreddit"
TEST_SUBREDDIT_2 = "test subreddit 2"
TEST_SUBREDDIT_3 = "test subreddit 3"
TEST_SUBREDDIT_4 = "test subreddit 4"
TEST_REDDIT_ID = "test reddit id"

CLIENT_ID = "mock_id"
CLIENT_SECRET = "mock_secret"

TEST_DIRECT_LINK = "http://i.imgur.com/abcdef.pdf"

TEST_IMAGE_LINK = "http://imgur.com/abcdef"

ALBUM_1 = 'album id 1'
TEST_ALBUM_LINK_1 = "http://imgur.com/a/{0}".format(ALBUM_1)

ALBUM_2 = 'album id 2'
TEST_ALBUM_LINK_2 = "http://imgur.com/a/{0}".format(ALBUM_2)

GALLERY_1 = 'gallery id 1'
TEST_GALLERY_LINK_1 = "http://imgur.com/g/{0}".format(GALLERY_1)

IMAGE_1 = 'image id 1'
TEST_IMAGE_LINK_1 = "http://imgur.com/{0}".format(IMAGE_1)


class RedditMeme(object):
    def __init__(self, sub=TEST_SUBREDDIT, url=TEST_LINK, id_=TEST_REDDIT_ID):
            self.subreddit = sub
            self.url = url
            self.id = id_


@pytest.fixture
def meme():
    return Meme(RedditMeme())


@pytest.fixture
def dank_meme():
    return DankMeme(RedditMeme())


@pytest.fixture
def imgur_direct_meme():
    ImgurMeme.set_credentials(CLIENT_ID, CLIENT_SECRET)
    return ImgurMeme(RedditMeme(url=TEST_DIRECT_LINK))


@pytest.fixture
def imgur_image_meme():
    ImgurMeme.set_credentials(CLIENT_ID, CLIENT_SECRET)
    return ImgurMeme(RedditMeme(url=TEST_IMAGE_LINK))


@pytest.fixture
def imgur_image_meme_2():
    ImgurMeme.set_credentials(CLIENT_ID, CLIENT_SECRET)
    return ImgurMeme(RedditMeme(sub=TEST_SUBREDDIT_4, url=TEST_IMAGE_LINK_1))


@pytest.fixture
def imgur_album_meme_1():
    ImgurMeme.set_credentials(CLIENT_ID, CLIENT_SECRET)
    return ImgurMeme(RedditMeme(url=TEST_ALBUM_LINK_1))


@pytest.fixture
def imgur_album_meme_2():
    ImgurMeme.set_credentials(CLIENT_ID, CLIENT_SECRET)
    return ImgurMeme(RedditMeme(sub=TEST_SUBREDDIT_2, url=TEST_ALBUM_LINK_2))


@pytest.fixture
def imgur_gallery_meme_1():
    ImgurMeme.set_credentials(CLIENT_ID, CLIENT_SECRET)
    return ImgurMeme(RedditMeme(sub=TEST_SUBREDDIT_3, url=TEST_GALLERY_LINK_1))


@pytest.fixture
def client():
    with patch("dankbot.memes.ImgurClient") as client:
        client.return_value = client
        client.get_image.return_value = client
        client.gallery_item.return_value = client
        client.get_album.return_value = client

        yield client


def test_meme(meme):
    """ Tests the base Meme class
    """
    assert meme.link == TEST_LINK
    assert meme.source == TEST_SUBREDDIT
    assert str(meme) == TEST_LINK
    assert repr(meme) == "from {0}: {1}".format(TEST_SUBREDDIT, TEST_LINK)
    assert meme.format_for_slack() == repr(meme)


def test_dankmeme(dank_meme):
    """ Tests the DankMeme subclass
    """
    assert dank_meme.link == TEST_LINK
    assert dank_meme.source == TEST_SUBREDDIT
    assert str(dank_meme) == TEST_LINK
    assert repr(dank_meme) == "from {0}: {1}".format(TEST_SUBREDDIT, TEST_LINK)
    assert dank_meme.format_for_slack() == repr(dank_meme)


def test_ImgurMeme_credential_setting():
    """ Tests the ImgurMeme subclass credential setting
    """
    reddit_meme = RedditMeme(url=TEST_IMAGE_LINK)

    ImgurMeme.set_credentials(CLIENT_ID, CLIENT_SECRET)

    i_meme = ImgurMeme(reddit_meme)

    assert i_meme.client_id == CLIENT_ID
    assert i_meme.client_secret == CLIENT_SECRET


def test_ImgurMeme_get_client_exception(client):
    """ Test the imgur client creation functionality
    """
    # Setup the ImgurMeme object
    ImgurMeme.set_credentials(None, None)

    i_meme = ImgurMeme(RedditMeme(url=TEST_IMAGE_LINK))

    with pytest.raises(ValueError) as excstr:
        i_meme.digest()

    assert "Client ID" in str(excstr.value)
    assert "Secret" in str(excstr.value)
    assert not client.called


def test_ImgurMeme_get_client(client):
    """ Test the imgur client creation functionality
    """
    # Setup the ImgurMeme object
    ImgurMeme.set_credentials(CLIENT_ID, CLIENT_SECRET)

    ImgurMeme(RedditMeme(url=TEST_IMAGE_LINK)).digest()

    assert client.called


def test_ImgurMeme_direct_link(client, imgur_direct_meme):
    """ Test Imgur Meme using a direct link to an image
    """
    # Digest the link
    imgur_direct_meme.digest()

    # Slack formating
    slack_str = imgur_direct_meme.format_for_slack()

    assert not client.called
    assert not client.get_image.called
    assert not client.gallery_item.called
    assert imgur_direct_meme.link_type is ImgurMeme.DIRECT_LINK
    assert imgur_direct_meme.image_count is None
    assert imgur_direct_meme.first_image_link is None
    assert TEST_SUBREDDIT in slack_str
    assert TEST_DIRECT_LINK in slack_str
    assert "more at" not in slack_str


def test_ImgurMeme_album_01(client, imgur_album_meme_1):
    """ Test Imgur Meme using a link to an album
    """
    image_count = 10
    fake_link = 'fake link'
    client.images_count = image_count
    client.images = [{'link': fake_link}, ]

    # Digest the link
    imgur_album_meme_1.digest()

    # Slack formating
    slack_str = imgur_album_meme_1.format_for_slack()

    assert client.called
    assert not client.get_image.called
    assert not client.gallery_item.called
    assert imgur_album_meme_1.link_type is ImgurMeme.ALBUM_LINK
    client.get_album.assert_called_with(ALBUM_1)
    assert imgur_album_meme_1.image_count == image_count
    assert imgur_album_meme_1.first_image_link == fake_link
    assert TEST_SUBREDDIT in slack_str
    assert TEST_ALBUM_LINK_1 in slack_str
    assert fake_link in slack_str
    assert "more at" in slack_str


def test_ImgurMeme_album_02(client, imgur_album_meme_2):
    image_count = 5
    fake_link = 'fake link 2'
    client.images_count = image_count
    client.images = [{'link': fake_link}, ]

    # Digest the link
    imgur_album_meme_2.digest()

    assert client.called
    assert not client.get_image.called
    assert not client.gallery_item.called
    assert imgur_album_meme_2.link_type is ImgurMeme.ALBUM_LINK
    client.get_album.assert_called_with(ALBUM_2)
    assert imgur_album_meme_2.image_count == image_count
    assert imgur_album_meme_2.first_image_link == fake_link


def test_ImgurMeme_gallery_01(client, imgur_gallery_meme_1):
    client.is_album = True

    image_count = 15
    fake_link = 'fake link 3'
    client.images_count = image_count
    client.images = [{'link': fake_link}, ]

    # Digest the link
    imgur_gallery_meme_1.digest()

    # Slack formating
    slack_str = imgur_gallery_meme_1.format_for_slack()

    assert client.called
    assert not client.get_image.called
    assert not client.album_item.called
    assert imgur_gallery_meme_1.link_type is ImgurMeme.GALLERY_LINK
    client.gallery_item.assert_called_with(GALLERY_1)
    assert imgur_gallery_meme_1.image_count == image_count
    assert imgur_gallery_meme_1.first_image_link == fake_link
    assert TEST_SUBREDDIT_3 in slack_str
    assert TEST_GALLERY_LINK_1 in slack_str
    assert fake_link in slack_str
    assert "more at" in slack_str


def test_ImgurMeme_gallery_02(client, imgur_gallery_meme_1):
    # Setup the mock object
    client.is_album = False
    other_fake_link = "fake link solo"
    client.link = other_fake_link

    image_count = 15
    fake_link = 'fake link 4'
    client.images_count = image_count
    client.images = [{'link': fake_link}, ]

    # Digest the link
    imgur_gallery_meme_1.digest()

    assert client.called
    assert not client.get_image.called
    assert not client.album_item.called
    assert imgur_gallery_meme_1.link_type is ImgurMeme.GALLERY_LINK
    client.gallery_item.assert_called_with(GALLERY_1)
    assert imgur_gallery_meme_1.image_count == 0
    assert imgur_gallery_meme_1.first_image_link == other_fake_link


def test_ImgurMeme_image_01(client, imgur_image_meme_2):
    # Setup the mock object
    client.is_album = False
    other_fake_link = "fake image link"
    client.link = other_fake_link

    # Digest the link
    imgur_image_meme_2.digest()

    # Slack formating
    slack_str = imgur_image_meme_2.format_for_slack()

    assert client.called
    assert not client.album_item.called
    assert not client.gallery_item.called
    assert imgur_image_meme_2.link_type is ImgurMeme.IMAGE_LINK
    client.get_image.assert_called_with(IMAGE_1)
    assert imgur_image_meme_2.image_count == 0
    assert imgur_image_meme_2.first_image_link == other_fake_link
    assert TEST_SUBREDDIT_4 in slack_str
    assert other_fake_link in slack_str
    assert "more at" not in slack_str


def test_undigested_exception(client, imgur_image_meme):
    """ Verify UndigestedError gets raised if digest hasn't been called
    """
    with pytest.raises(UndigestedError) as excstr:
        imgur_image_meme.format_for_slack()

    assert "You must digest" in str(excstr.value)


def test_bad_link_type_exception(client, imgur_image_meme):
    """ Verify exception is thrown if link type is not recognized
    """
    imgur_image_meme._digested = True

    with pytest.raises(TypeError) as excstr:
        imgur_image_meme.format_for_slack()

    assert "Imgur link type not recognized" in str(excstr.value)
