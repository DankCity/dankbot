import pytest

from tests import RedditMeme, test_vars as tv
from dankbot.memes import ImgurMeme, UndigestedError


def test_meme(meme):
    """ Tests the base Meme class
    """
    assert meme.link == tv['TEST_LINK']
    assert meme.source == tv['TEST_SUBREDDIT']
    assert str(meme) == tv['TEST_LINK']
    assert repr(meme) == "from {0}: {1}".format(tv['TEST_SUBREDDIT'], tv['TEST_LINK'])
    assert meme.format_for_slack() == repr(meme)


def test_dankmeme(dank_meme):
    """ Tests the DankMeme subclass
    """
    assert dank_meme.link == tv['TEST_LINK']
    assert dank_meme.source == tv['TEST_SUBREDDIT']
    assert str(dank_meme) == tv['TEST_LINK']
    assert repr(dank_meme) == "from {0}: {1}".format(tv['TEST_SUBREDDIT'], tv['TEST_LINK'])
    assert dank_meme.format_for_slack() == repr(dank_meme)


def test_ImgurMeme_credential_setting():
    """ Tests the ImgurMeme subclass credential setting
    """
    reddit_meme = RedditMeme(url=tv['TEST_IMAGE_LINK'])

    ImgurMeme.set_credentials(tv['CLIENT_ID'], tv['CLIENT_SECRET'])

    i_meme = ImgurMeme(reddit_meme)

    assert i_meme.client_id == tv['CLIENT_ID']
    assert i_meme.client_secret == tv['CLIENT_SECRET']


def test_ImgurMeme_get_client_exception(client):
    """ Test the imgur client creation functionality
    """
    # Setup the ImgurMeme object
    ImgurMeme.set_credentials(None, None)

    i_meme = ImgurMeme(RedditMeme(url=tv['TEST_IMAGE_LINK']))

    with pytest.raises(ValueError) as excstr:
        i_meme.digest()

    assert "Client ID" in str(excstr.value)
    assert "Secret" in str(excstr.value)
    assert not client.called


def test_ImgurMeme_get_client(client):
    """ Test the imgur client creation functionality
    """
    # Setup the ImgurMeme object
    ImgurMeme.set_credentials(tv['CLIENT_ID'], tv['CLIENT_SECRET'])

    ImgurMeme(RedditMeme(url=tv['TEST_IMAGE_LINK'])).digest()

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
    assert tv['TEST_SUBREDDIT'] in slack_str
    assert tv['TEST_DIRECT_LINK'] in slack_str
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
    client.get_album.assert_called_with(tv['ALBUM_1'])
    assert imgur_album_meme_1.image_count == image_count
    assert imgur_album_meme_1.first_image_link == fake_link
    assert tv['TEST_SUBREDDIT'] in slack_str
    assert tv['TEST_ALBUM_LINK_1'] in slack_str
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
    client.get_album.assert_called_with(tv['ALBUM_2'])
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
    client.gallery_item.assert_called_with(tv['GALLERY_1'])
    assert imgur_gallery_meme_1.image_count == image_count
    assert imgur_gallery_meme_1.first_image_link == fake_link
    assert tv['TEST_SUBREDDIT_3'] in slack_str
    assert tv['TEST_GALLERY_LINK_1'] in slack_str
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
    client.gallery_item.assert_called_with(tv['GALLERY_1'])
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
    client.get_image.assert_called_with(tv['IMAGE_1'])
    assert imgur_image_meme_2.image_count == 0
    assert imgur_image_meme_2.first_image_link == other_fake_link
    assert tv['TEST_SUBREDDIT_4'] in slack_str
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
