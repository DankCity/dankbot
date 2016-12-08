test_vars = {
    "TEST_LINK": "test meme link",
    "TEST_SUBREDDIT": "test subreddit",
    "TEST_SUBREDDIT_2": "test subreddit 2",
    "TEST_SUBREDDIT_3": "test subreddit 3",
    "TEST_SUBREDDIT_4": "test subreddit 4",
    "TEST_REDDIT_ID": "test reddit id",

    "CLIENT_ID": "mock_id",
    "CLIENT_SECRET": "mock_secret",

    "TEST_DIRECT_LINK": "http://i.imgur.com/abcdef.pdf",

    "TEST_IMAGE_LINK": "http://imgur.com/abcdef",

    "ALBUM_1": 'album id 1',
    "TEST_ALBUM_LINK_1": "http://imgur.com/a/album id 1",

    "ALBUM_2": 'album id 2',
    "TEST_ALBUM_LINK_2": "http://imgur.com/a/album id 2",

    "GALLERY_1": 'gallery id 1',
    "TEST_GALLERY_LINK_1": "http://imgur.com/g/gallery id 1",

    "IMAGE_1": 'image id 1',
    "TEST_IMAGE_LINK_1": "http://imgur.com/image id 1",
}

TS = test_vars['TEST_SUBREDDIT']
TL = test_vars['TEST_LINK']
TRD = test_vars['TEST_REDDIT_ID']


class RedditMeme(object):
    def __init__(self, sub=TS, url=TL, id_=TRD, over_18=False):
            self.subreddit = sub
            self.url = url
            self.id = id_
            self.over_18 = over_18
