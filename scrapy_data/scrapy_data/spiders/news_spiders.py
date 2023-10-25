from pathlib import Path

import scrapy


class WPSpider(scrapy.Spider):
    
    name = "wp_spider"
    news_class = 'i2PrHTUx'
    next_page_class = 'i1xRndDA i1ZgYxIQ i2zbd-HY'

    # for this url there is a parse method called
    start_urls = [
            "https://wiadomosci.wp.pl",
        ]

    def parse(self, response):
        
        news_list = response.xpath(f'//a[@class="{self.news_class}"]')
        self.log(f"Found newses: {len(news_list)}")

        for news in news_list:

            link = news.attrib["href"]
            title = news.attrib["title"]

            yield {"title": title, "link": link}

        next_page = response.xpath(f'//a[@class="{self.next_page_class}"]')
        next_page = next_page.attrib["href"]

        if next_page is not None:

            page_num = int(next_page.strip('/'))
            next_page = response.urljoin(next_page)

            if page_num < 3:
                yield scrapy.Request(next_page, callback=self.parse)
