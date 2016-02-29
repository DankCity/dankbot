from dankbot.memes import Meme


def test_meme():
    new_meme = Meme("test link", "test source")

    assert new_meme.link == "test link"
    assert new_meme.source == "test source"
