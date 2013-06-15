# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

"""
We crawl the name of the company, its website link,
its foundation year and its country. Besides we provide
as key the url to its Linkedin page.
Missing attributes are handled as empty strings ('')
"""
class LinkedinItem(Item):
    name = Field()
    website_link = Field()
    foundation_year = Field()
    country = Field()
    _id = Field()
