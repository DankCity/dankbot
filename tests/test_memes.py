import pytest
from unittest.mock import patch

from dankbot.memes import ImgurMeme, DankMeme, Meme


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
    """ Test Imgur Meme with using a direct link to an image
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

    assert not client_mock.called


def test_ImgurMeme_album_01():
    pass


def test_ImgurMeme_album_02():
    pass


def test_ImgurMeme_gallery_01():
    pass


def test_ImgurMeme_gallery_02():
    pass


def test_ImgurMeme_format_for_slack():
    pass
