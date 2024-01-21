# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from mongoDB_handler import mongoDB_handler
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class NewsReaderPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        mongoDB_settings = {}
        mongoDB_settings["server"] = str(settings.get("MONGODB_SERVER"))
        mongoDB_settings["port"] = int(settings.get("MONGODB_PORT"))
        mongoDB_settings["db"] = str(settings.get("MONGODB_DB"))
        mongoDB_settings["collection"] = str(
            settings.get("MONGODB_COLLECTION")
        )

        # Create an instance of the pipeline with the settings
        return cls(mongoDB_settings)

    def __init__(self, mongoDB_settings):
        settings = mongoDB_settings
        self.collection = mongoDB_handler(mongoDB_settings=settings)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        required_keys = ["title", "text", "date"]
        missing_keys = []

        for key in required_keys:
            if not adapter.get(key):
                missing_keys.append(key)

        if missing_keys:
            raise DropItem(f"Missing {missing_keys} in {item}")
        else:
            self.collection.insert(dict(item))
            return item

    def close_spider(self, spider):
        self.collection.drop_duplicates(["title", "date"])
