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

        page_to_follow = response.attrib["href"]

        #app > div > div > div:nth-child(1) > div.content.i2d9_HLt > div > div > div > div.i3P8PD9G.h1lqk8w > div > div > div.teasersListing.glonews.icT1MaIp.i1pOcmQ4 > div > div > div > div.i2eMLotm.i2bCtMbs.i2SEFzLe.i2N4iaRc.teaserBgColor > div > a

        # working for specific news
        # response.xpath('//*[@id="app"]/div/div/div[1]/div[6]/div/div/div/div[2]/div/div/div[1]/div/div/div/div[1]/div/a')

        #app > div > div > div:nth-child(1) > div.content.i2d9_HLt > div > div > div > div.i3P8PD9G.h1lqk8w > div > div > div.teasersListing.glonews.icT1MaIp.i1pOcmQ4 > div > div > div

        # wroking for all news section
        # //*[@id="app"]/div/div/div[1]/div[6]/div/div/div/div[2]/div/div/div[1]/div/div/div