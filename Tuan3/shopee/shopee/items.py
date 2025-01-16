# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopeeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_type = scrapy.Field()
    product_stock = scrapy.Field()
    product_brand = scrapy.Field()
    product_size = scrapy.Field()
    product_forGame = scrapy.Field()
    product_TV = scrapy.Field()
    product_status =scrapy.Field()
    product_warranty_period = scrapy.Field()
    product_warranty_type = scrapy.Field()
    product_weight = scrapy.Field()
    product_ship_from = scrapy.Field()
    pass
