from pathlib import Path

import scrapy


class WPSpider(scrapy.Spider):
    name = "wp_spider"

    # for this url there is a parse method called
    start_urls = [
            "https://wiadomosci.wp.pl",
        ]

    def parse(self, response):
        filename = f"test.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")