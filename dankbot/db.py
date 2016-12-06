import os
from appdirs import user_data_dir
import logging
import sqlite3 as lite
from os.path import join
from contextlib import closing

from dankbot import APPNAME, APPAUTHOR

logger = logging.getLogger(__name__)

DB_NAME = 'dankbot.db'


class DB(object):
    db_dir = None
    db_path = None
    def __init__(self, db_dir=None, create_db=False):
        self.db_dir = db_dir or user_data_dir(APPNAME, APPAUTHOR)
        self.db_path =join(self.db_dir, DB_NAME)

        if create_db is True:
            self._create_db_and_table()

    def _query(self, query, args=None):
        if not args:
            args = dict()

        with lite.connect(self.db_path) as con, closing(con.cursor()) as cur:
            cur.execute(query, args)
            return cur.fetchall()

    def _create_db_and_table(self):
        """ Create the database and table if it doesn't exist
        """
        if os.path.exists(self.db_path):
            logger.info("Will not create database: already exists at:"
                        " {0}".format(self.db_path))
            return

        # Create the data directory if it doesn't exist
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        logger.info("Creating database at: {0}".format(self.db_path))

        query = """CREATE TABLE IF NOT EXISTS memes (
            id INTEGER PRIMARY KEY,
            link VARCHAR(255) NOT NULL,
            source VARCHAR(255) NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
            );"""

        return self._query(query)

    def add_to_collection(self, meme):
        """ Add meme to database collection
        """

        query = """INSERT INTO memes (link, source)
                   VALUES(?,?)"""

        self._query(query, (meme.link, meme.source))

    def in_collection(self, meme):
        query = "SELECT * FROM memes WHERE link=:link"

        try:
            resp = self._query(query, {'link': meme.link})
        except UnicodeEncodeError:
            # Indicates a link with oddball characters, just ignore it
            resp = True

            log = "Bad character in meme: {0}"
            self.logger.exception(log.format(meme))

        return True if resp else False


if __name__ == "__main__":
    global APPNAME
    global APPAUTHOR

    APPNAME = 'dankbot'
    APPAUTHOR = 'levi'

    print("About to check SQLite version")
    db = DB()
    # print(db._query('SELECT SQLITE_VERSION()'))
    print("About to create table")
    print(db.create_db_and_table())
