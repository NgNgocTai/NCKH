import scrapy


class FashionspiderSpider(scrapy.Spider):
    name = "fashionSpider"
    start_urls = ["https://www.marksandspencer.com/denim-maxi-skirt/p/clp60721306"]

    def parse(self, response):
        pass
