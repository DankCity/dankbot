class Meme(object):
    """
    Base class for meme objects
    """
    def __init__(self, link, source):
        self.link = link
        self.source = source

    def __str__(self):
        return str(self.link)

    def __repr__(self):
        return "{0} from {1}".format(self.link, self.source)

    def format_for_slack(self):
        return repr(self)


class DankMeme(Meme):
    """
    Regular, run of the mill means
    """
    pass


class ImgurGallery(Meme):
    """
    Class specific to meme's from Imgur.com
    """
    pass
