"""
This file contains logic of application
"""

import subprocess
import os
from mongoDB_handler import mongoDB_handler
from website_connection_checks import WpChecks


if __name__ == "__main__":

    spiders_to_run = ["wp_spider"]
    parent_dir = os.getcwd()
    scrapy_path = os.path.join(parent_dir, "scrapy_project")

    wp_checks = WpChecks()
    css_prefix = wp_checks.get_css_prefix()

    # for spider in spiders_to_run:
    #     scrapy_command = ["scrapy", "crawl", spider, "-O",
    #                        "test.jsonl", "-a", f"prefix={css_prefix}"]
    #     subprocess.run(scrapy_command, cwd=scrapy_path)
    
    print("Connecting to MongoDB")
    mongo = mongoDB_handler('localhost', 27017,
                            db_name="news-catalog",
                            collection_name='newses'
                            )
    doc1 = {"a": 1, "b":2}
    doc2 = {"a": 2, "c":3}
    doc3 = {"b": 4, "c":5}
    mongo.insert([doc1, doc2])
    mongo.insert(doc3)

    items = mongo.collection.find()
    for item in items:
        print(item)
    print("Connected to MongoDB")
