from pymongo import MongoClient

from .config import get_config
from .db import Database


class MongoDatabase(Database):
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        config = get_config()

        self.client = MongoClient(config['db.dsn'])
        self.db = self.client[config['db.database']]

    def insert(self, collection, document):
        # if not self.db:
        self.connect()

        return self.db[collection].insert_one(document).inserted_id
