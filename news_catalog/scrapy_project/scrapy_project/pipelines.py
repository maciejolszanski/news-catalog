# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging

from scrapy.exceptions import DropItem
from mongoDB_handler import mongoDB_handler

class NewsReaderPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        mongoDB_settings = {}
        mongoDB_settings['server'] = str(settings.get('MONGODB_SERVER'))
        mongoDB_settings['port'] = int(settings.get('MONGODB_PORT'))
        mongoDB_settings['db'] = str(settings.get('MONGODB_DB'))
        mongoDB_settings['collection'] = str(settings.get('MONGODB_COLLECTION'))

        # Create an instance of the pipeline with the settings
        return cls(mongoDB_settings)
    
    def __init__(self, mongoDB_settings):
        settings = mongoDB_settings
        self.collection = mongoDB_handler(mongoDB_settings=settings)

    def process_item(self, item, spider):
        valid = True
        if valid:
            self.collection.insert(dict(item))

        return item
