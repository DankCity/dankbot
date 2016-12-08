import os
from appdirs import user_data_dir
import sqlite3 as lite
from os.path import join
from contextlib import closing

from dankbot import APPNAME, APPAUTHOR

DB_NAME = 'dankbot.db'


class DB(object):
    db_dir = None
    db_path = None
    db_con = None

    def __init__(self, logger, db_dir=None, create_db=False):
        self.logger = logger

        self.db_dir = db_dir or user_data_dir(APPNAME, APPAUTHOR)
        self.db_path = join(self.db_dir, DB_NAME)

        if create_db is True:
            self._create_db_and_table()

    def _query(self, query, args=None):
        if not args:
            args = dict()

        if self.db_con is None:
            self.db_con = lite.connect(self.db_path)

        with self.db_con, closing(self.db_con.cursor()) as cur:
            cur.execute(query, args)
            return cur.fetchall()

    def _create_db_and_table(self):
        """ Create the database and table if it doesn't exist
        """
        if os.path.exists(self.db_path):  # pragma: no cover
            self.logger.info("Will not create database: already exists at:"
                             " {0}".format(self.db_path))  # pylint: disable=W1202
            return

        # Create the data directory if it doesn't exist
        if not os.path.exists(self.db_dir):  # pragma: no cover
            os.makedirs(self.db_dir)

        self.logger.info("Creating database at: {0}".format(self.db_path))  # pylint: disable=W1202

        query = """CREATE TABLE IF NOT EXISTS memes (
            reddit_id VARCHAR(255) PRIMARY KEY NOT NULL,
            source VARCHAR(255) NOT NULL,
            link VARCHAR(255) NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
            );"""

        return self._query(query)

    def add_to_collection(self, meme):
        """ Add meme to database collection
        """

        query = """INSERT INTO memes (reddit_id, source, link)
                   VALUES(?,?,?)"""

        self._query(query, (meme.reddit_id, meme.source, meme.link))

    def in_collection(self, meme):
        query = "SELECT * FROM memes WHERE reddit_id=:reddit_id"

        try:
            resp = self._query(query, {'reddit_id': meme.reddit_id})
        except UnicodeEncodeError:  # pragma: no cover
            # Indicates a link with oddball characters, just ignore it
            resp = True

            log = "Bad character in meme: {0}"
            self.logger.exception(log.format(meme))

        return True if resp else False

    def update_collection(self, meme):
        """ Update the last_seen column with the current timestamp
        """
        query = """UPDATE memes SET last_seen=(CURRENT_TIMESTAMP)
                   WHERE reddit_id=(:id)"""

        self._query(query, {'id': meme.reddit_id})
