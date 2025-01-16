# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    type_= scrapy.Field()
    tax = scrapy.Field()
    stock = scrapy.Field()
    reviews = scrapy.Field()
    
    pass
