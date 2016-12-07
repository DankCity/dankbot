from imgurpython import ImgurClient


class UndigestedError(Exception):
    pass


class Meme(object):  # pylint: disable=R0903
    """
    Base class for meme objects
    """
    def __init__(self, meme):
        self.source = str(meme.subreddit)
        self.reddit_id = meme.id
        self.link = meme.url

    def __str__(self):
        return str(self.link)

    def __repr__(self):
        return "from {0}: {1}".format(self.source, self.link)

    def format_for_slack(self):
        return repr(self)


class DankMeme(Meme):  # pylint: disable=too-few-public-methods
    """
    Regular, run of the mill memes
    """
    pass


class ImgurMeme(Meme):
    """
    Base class for Imgur meme types
    """
    # Imgur link types
    DIRECT_LINK = "direct link"
    IMAGE_LINK = "image link"
    ALBUM_LINK = "album link"
    GALLERY_LINK = "gallery link"

    client_id = None
    client_secret = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image_count = None
        self.first_image_link = None

        self.link_type = None
        self._digested = False

    def _get_client(self):
        """
        Creates and returns an ImgurClient object
        """
        if not all([self.client_id, self.client_secret]):
            raise ValueError("Client ID and Secret must be set first")

        return ImgurClient(self.client_id, self.client_secret)

    @classmethod
    def set_credentials(cls, client_id, client_secret):
        """
        Class method for setting the Imgur API client ID and client secret
        """
        cls.client_id = client_id
        cls.client_secret = client_secret

    def format_for_slack(self):
        """
        Formats meme into a string to be posted to slack chat
        """
        if not self._digested:
            exc_str = "You must digest ImgurMeme objects before attempting to" + \
                      "run img_obj.format_for_slack(). See img_obj.digest()"
            raise UndigestedError(exc_str)

        elif self.link_type == self.DIRECT_LINK:
            return "from {0}: {1}".format(self.source, self.link)

        elif self.link_type == self.IMAGE_LINK:
            return "from {0}: {1}".format(self.source, self.first_image_link)

        elif self.link_type == self.ALBUM_LINK or self.link_type == self.GALLERY_LINK:
            return_str = "from {0}: {1}".format(self.source, self.first_image_link)
            if self.image_count and self.image_count > 1:
                return_str += "\n{0} more at {1}".format(self.image_count - 1, self.link)
            return return_str

        else:
            exc_str = "Imgur link type not recognized: {0}"
            raise TypeError(exc_str.format(self.link_type))

    def digest(self):
        """
        Connects to Imgur API to collect more information about this meme
        """
        if "i.imgur.com/" in self.link:
            # Do nothing, since this is already just a direct link
            self.link_type = self.DIRECT_LINK

        elif "imgur.com/a/" in self.link or "imgur.com/album/" in self.link:
            # Link to an album
            self.link_type = self.ALBUM_LINK
            self._parse_as_album()

        elif "imgur.com/g/" in self.link or "imgur.com/gallery/" in self.link:
            # Link to a gallery
            self.link_type = self.GALLERY_LINK
            self._parse_as_gallery()

        else:
            # Must be an image
            self.link_type = self.IMAGE_LINK
            self._parse_as_image()

        self._digested = True

    def _parse_as_image(self):
        """
        Connects to Imgur to get more info on the image
        """
        # Entry point format: imgur.com/{image_id}
        image_id = self.link.split('/')[-1]

        # Remove file extension, if present
        image_id = image_id.split('.')[0]

        response = self._get_client().get_image(image_id)

        self.image_count = 0
        self.first_image_link = response.link

        return

    def _parse_as_gallery(self):
        """
        Connects to Imgur to get more info on the gallery
        """
        # Entry point format: imgur.com/gallery/{gallery_post_id}
        # Entry point format: imgur.com/gallery/{gallery_post_id}/new
        gallery_post_id = self.link.split('/new')[0].strip('/').split('/')[-1]
        response = self._get_client().gallery_item(gallery_post_id)

        if response.is_album:
            self.image_count = response.images_count
            self.first_image_link = response.images[0]['link']
        else:
            self.image_count = 0
            self.first_image_link = response.link

        return

    def _parse_as_album(self):
        """
        Connects to Imgur to get more info on the album
        """
        # Entry point format: imgur.com/a/{album_id}
        # Entry point format: imgur.com/a/{album_id}#{image_id}
        album_id = self.link.split('/')[-1].split("#")[0]
        response = self._get_client().get_album(album_id)

        self.image_count = response.images_count
        self.first_image_link = response.images[0]['link']

        return
