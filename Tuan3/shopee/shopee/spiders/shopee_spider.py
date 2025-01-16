import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import ShopeeItem

class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['shopee.vn']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        # 'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        yield SeleniumRequest(
            url="https://shopee.vn/M%C3%A0n-H%C3%ACnh-cat.11035954.11035961?page=0",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        # Sử dụng class 'contents' trong danh sách sản phẩm
        products = response.css('.shopee-search-item-result__item')
        for product in products:
            href = product.css('a.contents::attr(href)').get()
            if href:
                product_url = response.urljoin(href)
                yield SeleniumRequest(
                    url=product_url,
                    wait_time=5,
                    callback=self.parse_page
                )


    def parse_page(self, response):
        # Trích xuất dữ liệu từ trang chi tiết sản phẩm
        # items = ShopeeItem()
        # items['product_name'] = response.css('.WBVL_7 span::text').get()
        # items['product_price'] = response.css('.B67UQ0::text').get()
        # yield items
        yield {
            'product_name': response.css('.WBVL_7 span::text').get(),
            'product_price': response.css('.B67UQ0::text').get(),
        }