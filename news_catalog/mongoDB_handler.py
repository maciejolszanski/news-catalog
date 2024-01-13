"""
This file contains class that copes with MongoDB
"""

from pymongo import MongoClient


class mongoDB_handler:
    def __init__(self, mongoDB_settings):
        address = mongoDB_settings["server"]
        port = mongoDB_settings["port"]
        db_name = mongoDB_settings["db"]
        collection_name = mongoDB_settings["collection"]

        self.client = MongoClient(address, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data):
        if data.isintance(list):
            self.collection.insert_many(data)
        elif data.isintance(dict):
            self.collection.insert_one(data)
