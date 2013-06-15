# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class LinkedinItem(Item):
    name = Field()
    website_link = Field()
    foundation_year = Field()
    country = Field()
    _id = Field()
