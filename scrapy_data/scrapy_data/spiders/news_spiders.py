from pathlib import Path

import scrapy


class WPSpider(scrapy.Spider):
    
    name = "wp_spider"


    # for this url there is a parse method called
    # start_urls = [
    #         "https://wiadomosci.wp.pl",
    #     ]
    
    def start_requests(self):
        url = "https://wiadomosci.wp.pl"
        prefix = getattr(self, "prefix", None)
        if prefix is None:
            raise Exception("You need to pass a tag: prefix to classes.\n",
                            "To do it add prefix=<value e.g. i>")
        else:
            self.set_css_classes(prefix)
        yield scrapy.Request(url, self.parse)

    def set_css_classes(self, class_prefix):
        """
        WP webpage

        Args:
            prefix (_type_): _description_
        """

        self.news_class = f"{class_prefix}2PrHTUx"
        self.next_page_class = f"{class_prefix}1xRndDA {class_prefix}1ZgYxIQ {class_prefix}2zbd-HY"
        self.article_lead_class = f"article--lead {class_prefix}1HGmjUl"


    def parse(self, response):

        news_list = response.xpath(f'//a[@class="{self.news_class}"]')
        self.log(f"Found newses: {len(news_list)}")
        self.log(self.prefix)

        for news in news_list:

            link = news.attrib["href"]
            title = news.attrib["title"]

            yield scrapy.Request(response.urljoin(link), callback=self._parse_news_page)

            # yield {"title": title, "link": link}

        # Need to itarate over generator's results
        next_pages = self._next_page(response)
        for next_page in next_pages:
            yield next_page

    def _parse_news_page(self, response):

        lead = response.xpath(f'//div[@class="{self.article_lead_class}"]/p')
        lead = lead.xpath("string()").extract()[0]
        self.log(lead)

    def _next_page(self, response):
        """
        This function calls the next page and calls parse() to process it.

        Args:
            response (HtmlResponse): Response of HTML GET method on which 
                                     you want to find next_page button

        Yields:
            request: 
        """
            
        next_page_selector = response.xpath(f'//a[@class="{self.next_page_class}"]')

        for next_page in next_page_selector:
            next_page = next_page.attrib["href"]

            if next_page is not None:
                page_num = int(next_page.strip('/'))
                next_page = response.urljoin(next_page)

                if page_num < 5:
                    yield scrapy.Request(next_page, callback=self.parse)

        
