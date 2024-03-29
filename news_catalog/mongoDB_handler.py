"""
This file contains class that copes with MongoDB
"""

from pymongo import MongoClient
import datetime as dt


class MongoDBHandler:
    def __init__(self, mongoDB_settings):
        """Initalize database connetion

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

    def __str__(self):
        print(self.db)

    def insert(self, data):
        """Insert data to mongoDB collection.

        Args:
            data (list/dict): Data that are going to be inserted to collection.
        """
        if isinstance(data, list):
            self.collection.insert_many(data)
        elif isinstance(data, dict):
            self.collection.insert_one(data)

    def drop_duplicates(self, unique_keys):
        """Remove duplicates.

        Remove duplicates from collection considering only keys
        that should be unique.

        Args:
            unique_keys (list): Keys that should be unique in collection
        """
        duplicate_documents = self.collection.aggregate(
            [
                {
                    "$group": {
                        "_id": {key: f"${key}" for key in unique_keys},
                        "duplicates": {"$push": "$_id"},
                        "count": {"$sum": 1},
                    }
                },
                {"$match": {"count": {"$gt": 1}}},
            ]
        )

        for duplicate_group in duplicate_documents:
            # Keep one document (first one in the list) and delete the rest
            documents_to_delete = duplicate_group["duplicates"][1:]
            self.collection.delete_many({"_id": {"$in": documents_to_delete}})

    def get_data(self):
        """Get all items stored in MongoDB collection.

        Returns:
            items (list): List of items stored in MongoDB collection.
        """

        items = self.collection.find()
        return list(items)

    def get_max_date(self):
        """Get max date from collection.

        Returns:
            max_date (str): Max date from MongoDB collection.
        """
        pipeline = [{"$group": {"_id": None, "maxDate": {"$max": "$date"}}}]

        max_date = list(self.collection.aggregate(pipeline))[0]["maxDate"]

        if max_date is None:
            max_date = dt.datetime.now() - dt.timedelta(days=2)
            max_date = max_date.strftime("%Y-%m-%d")

        return max_date

    def update_item(self, item_id, field, value):
        self.collection.update_one({"_id": item_id}, {"$set": {field: value}})

        return self.collection.find({"_id": item_id})
