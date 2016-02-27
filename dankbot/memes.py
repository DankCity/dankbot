
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


class ImgurMeme(Meme):
    """
    Base class for Imgur meme types
    """
    client_id = None
    client_secret = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image_count = None
        self.first_image = None
        self.client_id = None
        self.client_secret = None

    @classmethod
    def set_credentials(cls, client_id, client_secret):
        """
        Class method for setting the Imgur API client ID and client secret
        """
        cls.client_id = client_id
        cls.client_secret = client_secret

    @classmethod
    def format_for_slack(cls):
        """
        Formats meme into a string to be posted to slack chat
        """
        pass

    def digest(self):
        """
        Connects to Imgur API to collect more information about this meme
        """
        if "i.imgur.com/" in self.link:
            # Do nothing, since this is already just a direct link
            pass
        elif "imgur.com/a/" in self.link or "imgur.com/album/" in self.link:
            pass
        elif "imgur.com/g/" in self.link or "imgur.com/gallery/" in self.link:
            pass
        else:
            pass
