# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class WPArticle(Item):
    
    title = Field()
    date = Field()
    author = Field()
    lead = Field()
    text = Field()
    url = Field()
