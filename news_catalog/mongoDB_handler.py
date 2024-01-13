"""
This file contains class that copes with MongoDB
"""

from pymongo import MongoClient


class mongoDB_handler:
    def __init__(self, mongoDB_settings):
        """
        Initalize database connetion

        Args:
            mongoDB_settings (dict): Settings that enable database connection.
                                     Required keys are:
                                        - server
                                        - port
                                        - db
                                        - collection
        """
        address = mongoDB_settings["server"]
        port = mongoDB_settings["port"]
        db_name = mongoDB_settings["db"]
        collection_name = mongoDB_settings["collection"]

        self.client = MongoClient(address, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data):
        """
        Function inserts data to mongoDB collection.

        Args:
            data (list/dict): Data that are going to be inserted to collection.
        """
        if data.isintance(list):
            self.collection.insert_many(data)
        elif data.isintance(dict):
            self.collection.insert_one(data)
