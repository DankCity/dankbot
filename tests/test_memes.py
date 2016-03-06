from dankbot.memes import Meme


def test_meme():
    test_link = "test link"
    test_source = "test source"

    new_meme = Meme(test_link, test_source)

    assert new_meme.link == test_link
    assert new_meme.source == test_source
    assert str(new_meme) == test_link
    assert repr(new_meme) == "from {0}: {1}".format(test_source, test_link)
    assert new_meme.format_for_slack() == repr(new_meme)
