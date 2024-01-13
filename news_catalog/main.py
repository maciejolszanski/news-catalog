"""
This file contains logic of application
"""

from website_connection_checks import WpChecks
from scrapy.crawler import CrawlerProcess
from scrapy_project.scrapy_project.spiders.news_spiders import WPSpider


def run_spider(prefix):
    """
    Function call scrapy spider that scrapes WP articles and saves data
    to MongoDB database.

    Args:
        prefix (str): css_prefix that will be used by a spider to define
                      proper css clasess.
    """
    settings = {
        "ITEM_PIPELINES": {
            "scrapy_project.scrapy_project.pipelines.NewsReaderPipeline": 100
        },
        "MONGODB_SERVER": "localhost",
        "MONGODB_PORT": 27017,
        "MONGODB_DB": "news-catalog",
        "MONGODB_COLLECTION": "newses",
    }
    process = CrawlerProcess(settings)

    # Add your spider to the process
    process.crawl(WPSpider, prefix=prefix)

    # Start the process
    process.start()


if __name__ == "__main__":
    wp_checks = WpChecks()
    css_prefix = wp_checks.get_css_prefix()

    run_spider(css_prefix)
