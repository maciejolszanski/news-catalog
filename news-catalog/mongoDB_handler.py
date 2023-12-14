"""
This file contains class that copes with MongoDB
"""

from pymongo import MongoClient


class mongoDB_handler():

    def __init__(self, address, port, db_name, collection_name):
        self.client = MongoClient(address, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data):
        
        if type(data) == list:
            self.collection.insert_many(data)
        elif type(data) == dict:
            self.collection.insert_one(data)
    
