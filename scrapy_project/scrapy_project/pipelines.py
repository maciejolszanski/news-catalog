# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging

from scrapy.exceptions import DropItem
from scrapy import settings


class NewsReaderPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        mongoDB_settings = {}
        mongoDB_settings['server'] = settings.get('MONGODB_SERVER')
        mongoDB_settings['port'] = settings.get('MONGODB_PORT')
        mongoDB_settings['db'] = settings.get('MONGODB_DB')
        mongoDB_settings['collection'] = settings.get('MONGODB_COLLECTION')

        # Create an instance of the pipeline with the settings
        return cls(mongoDB_settings)
    
    def __init__(self, mongoDB_settings):
        settings = mongoDB_settings
        connection = pymongo.MongoClient(
            settings['server'],
            settings['port']
        )
        db = connection[settings['db']]
        self.collection = db[settings['collection']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            # logging.info("Question added to MongoDB database!",
            #         level=log.DEBUG, spider=spider)
        return item
