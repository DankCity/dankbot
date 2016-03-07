import pytest
from unittest.mock import patch

from dankbot.memes import ImgurMeme, DankMeme, Meme, UndigestedError


def test_meme():
    """ Tests the base Meme class
    """
    test_link = "test meme link"
    test_source = "test meme source"

    new_meme = Meme(test_link, test_source)

    assert new_meme.link == test_link
    assert new_meme.source == test_source
    assert str(new_meme) == test_link
    assert repr(new_meme) == "from {0}: {1}".format(test_source, test_link)
    assert new_meme.format_for_slack() == repr(new_meme)


def test_dankmeme():
    """ Tests the DankMeme subclass
    """
    test_link = "test dank link"
    test_source = "test dank source"

    new_meme = DankMeme(test_link, test_source)

    assert new_meme.link == test_link
    assert new_meme.source == test_source
    assert str(new_meme) == test_link
    assert repr(new_meme) == "from {0}: {1}".format(test_source, test_link)
    assert new_meme.format_for_slack() == repr(new_meme)


def test_ImgurMeme_credential_setting():
    """ Tests the ImgurMeme subclass credential setting
    """
    test_link = "test imgur link"
    test_source = "test imgur source"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)

    i_meme = ImgurMeme(test_link, test_source)

    assert i_meme.client_id == client_id
    assert i_meme.client_secret == client_secret


@patch('dankbot.memes.ImgurClient')
def test_ImgurMeme_get_client(client_mock):
    """ Test the imgur client creation functionality
    """
    # Setup the ImgurMeme object
    test_link = "http://imgur.com/abcdef"
    test_source = "test imgur source"
    ImgurMeme.set_credentials(None, None)

    i_meme = ImgurMeme(test_link, test_source)

    with pytest.raises(ValueError) as excstr:
        i_meme.digest()

    assert "Client ID" in str(excstr.value)
    assert "Secret" in str(excstr.value)

    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)

    i_meme = ImgurMeme(test_link, test_source)
    i_meme.digest()

    assert client_mock.called


@patch("dankbot.memes.ImgurClient")
def test_ImgurMeme_direct_link(client_mock):
    """ Test Imgur Meme using a direct link to an image
    """
    # Setup the ImgurMeme object
    test_link = "http://i.imgur.com/abcdef.pdf"
    test_source = "test imgur source"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)

    i_meme = ImgurMeme(test_link, test_source)

    # Digest the link
    i_meme.digest()

    # Slack formating
    slack_str = i_meme.format_for_slack()

    assert not client_mock.called
    assert i_meme.link_type is ImgurMeme.DIRECT_LINK
    assert i_meme.image_count is None
    assert i_meme.first_image_link is None
    assert test_source in slack_str
    assert test_link in slack_str
    assert "more at" not in slack_str


@patch("dankbot.memes.ImgurClient")
def test_ImgurMeme_album_01(imgur_mock):
    """ Test Imgur Meme using a link to an album
    """
    # Setup the mock object
    imgur_mock.return_value = imgur_mock
    imgur_mock.get_album.return_value = imgur_mock

    image_count = 10
    fake_link = 'fake link'
    imgur_mock.images_count = image_count
    imgur_mock.images = [{'link': fake_link}, ]

    # Setup the ImgurMeme object
    album_id = 'albumid1'
    test_link = "http://imgur.com/a/{0}".format(album_id)
    test_source = "test imgur source"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)

    i_meme = ImgurMeme(test_link, test_source)

    # Digest the link
    i_meme.digest()

    # Slack formating
    slack_str = i_meme.format_for_slack()

    assert imgur_mock.called
    assert i_meme.link_type is ImgurMeme.ALBUM_LINK
    imgur_mock.get_album.assert_called_with(album_id)
    assert i_meme.image_count == image_count
    assert i_meme.first_image_link == fake_link
    assert test_source in slack_str
    assert test_link in slack_str
    assert fake_link in slack_str
    assert "more at" in slack_str


@patch("dankbot.memes.ImgurClient")
def test_ImgurMeme_album_02(imgur_mock):
    # Setup the mock object
    imgur_mock.return_value = imgur_mock
    imgur_mock.get_album.return_value = imgur_mock

    image_count = 5
    fake_link = 'fake link 2'
    imgur_mock.images_count = image_count
    imgur_mock.images = [{'link': fake_link}, ]

    # Setup the ImgurMeme object
    album_id = 'albumid2'
    test_link = "http://imgur.com/album/{0}".format(album_id)
    test_source = "test imgur source 2"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)

    i_meme = ImgurMeme(test_link, test_source)

    # Digest the link
    i_meme.digest()

    assert imgur_mock.called
    assert i_meme.link_type is ImgurMeme.ALBUM_LINK
    imgur_mock.get_album.assert_called_with(album_id)
    assert i_meme.image_count == image_count
    assert i_meme.first_image_link == fake_link


@patch("dankbot.memes.ImgurClient")
def test_ImgurMeme_gallery_01(imgur_mock):
    # Setup the mock object
    imgur_mock.return_value = imgur_mock
    imgur_mock.gallery_item.return_value = imgur_mock
    imgur_mock.is_album = True

    image_count = 15
    fake_link = 'fake link 3'
    imgur_mock.images_count = image_count
    imgur_mock.images = [{'link': fake_link}, ]

    # Setup the ImgurMeme object
    gallery_id = 'galleryid1'
    test_link = "http://imgur.com/g/{0}".format(gallery_id)
    test_source = "test imgur source 3"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)

    i_meme = ImgurMeme(test_link, test_source)

    # Digest the link
    i_meme.digest()

    # Slack formating
    slack_str = i_meme.format_for_slack()

    assert imgur_mock.called
    assert i_meme.link_type is ImgurMeme.GALLERY_LINK
    imgur_mock.gallery_item.assert_called_with(gallery_id)
    assert i_meme.image_count == image_count
    assert i_meme.first_image_link == fake_link
    assert test_source in slack_str
    assert test_link in slack_str
    assert fake_link in slack_str
    assert "more at" in slack_str


@patch("dankbot.memes.ImgurClient")
def test_ImgurMeme_gallery_02(imgur_mock):
    # Setup the mock object
    imgur_mock.return_value = imgur_mock
    imgur_mock.gallery_item.return_value = imgur_mock
    imgur_mock.is_album = False
    other_fake_link = "fake link solo"
    imgur_mock.link = other_fake_link

    image_count = 15
    fake_link = 'fake link 4'
    imgur_mock.images_count = image_count
    imgur_mock.images = [{'link': fake_link}, ]

    # Setup the ImgurMeme object
    gallery_id = 'galleryid1'
    test_link = "http://imgur.com/gallery/{0}".format(gallery_id)
    test_source = "test imgur source 3"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)

    i_meme = ImgurMeme(test_link, test_source)

    # Digest the link
    i_meme.digest()

    assert imgur_mock.called
    assert i_meme.link_type is ImgurMeme.GALLERY_LINK
    imgur_mock.gallery_item.assert_called_with(gallery_id)
    assert i_meme.image_count == 0
    assert i_meme.first_image_link == other_fake_link


@patch("dankbot.memes.ImgurClient")
def test_ImgurMeme_image_01(imgur_mock):
    # Setup the mock object
    imgur_mock.return_value = imgur_mock
    imgur_mock.get_image.return_value = imgur_mock
    imgur_mock.is_album = False
    other_fake_link = "fake image link"
    imgur_mock.link = other_fake_link

    # Setup the ImgurMeme object
    image_id = 'imageid1'
    test_link = "http://imgur.com/{0}".format(image_id)
    test_source = "test imgur source 4"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)

    i_meme = ImgurMeme(test_link, test_source)

    # Digest the link
    i_meme.digest()

    # Slack formating
    slack_str = i_meme.format_for_slack()

    assert imgur_mock.called
    assert i_meme.link_type is ImgurMeme.IMAGE_LINK
    imgur_mock.get_image.assert_called_with(image_id)
    assert i_meme.image_count == 0
    assert i_meme.first_image_link == other_fake_link
    assert test_source in slack_str
    assert other_fake_link in slack_str
    assert "more at" not in slack_str


def test_undigested_exception():
    """ Verify UndigestedError gets raised if digest hasn't been called
    """
    # Setup the ImgurMeme object
    image_id = 'imageid1'
    test_link = "http://imgur.com/{0}".format(image_id)
    test_source = "test imgur source 4"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)
    i_meme = ImgurMeme(test_link, test_source)

    with pytest.raises(UndigestedError) as excstr:
        i_meme.format_for_slack()

    assert "You must digest" in str(excstr.value)


def test_bad_link_type_exception():
    """ Verify exception is thrown if link type is not recognized
    """
    image_id = 'imageid1'
    test_link = "http://imgur.com/{0}".format(image_id)
    test_source = "test imgur source 4"
    client_id = "mock_id"
    client_secret = "mock_secret"

    ImgurMeme.set_credentials(client_id, client_secret)
    i_meme = ImgurMeme(test_link, test_source)
    i_meme._digested = True

    with pytest.raises(TypeError) as excstr:
        i_meme.format_for_slack()

    assert "Imgur link type not recognized" in str(excstr.value)
