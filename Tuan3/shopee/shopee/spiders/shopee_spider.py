# import scrapy
# from scrapy_selenium import SeleniumRequest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

# class ShopeeSpider(scrapy.Spider):
#     name = 'shopee'
#     allowed_domains = ['shopee.vn']

#     def start_requests(self):
#         yield SeleniumRequest(
#             url="https://shopee.vn/M%C3%A0n-H%C3%ACnh-cat.11035954.11035961?page=0",
#             wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '.shopee-search-item-result__item')),
#             callback=self.parse
#         )

#     def parse(self, response):
#         # Sử dụng class 'contents' trong danh sách sản phẩm
#         products = response.css('.shopee-search-item-result__item')
#         for product in products:
#             href = product.css('a.contents::attr(href)').get()
#             if href:
#                 product_url = response.urljoin(href)
#                 yield SeleniumRequest(
#                     url=product_url,
#                     wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '.WBVL_7 span')),
#                     callback=self.parse_page
#                 )

#     def parse_page(self, response):
#         # Trích xuất dữ liệu từ trang chi tiết sản phẩm
#         yield {
#             'product_name': response.css('.WBVL_7 span::text').get(),
#             'product_price': response.css('.B67UQ0::text').get(),
#         }

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['shopee.vn']

    def start_requests(self):
        # Bắt đầu truy vấn với SeleniumRequest
        yield SeleniumRequest(
            url="https://shopee.vn/M%C3%A0n-H%C3%ACnh-cat.11035954.11035961?page=0",
            wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '.shopee-search-item-result__item')),
            callback=self.parse
        )

    def parse(self, response):
        # Lấy danh sách các sản phẩm
        products = response.css('.shopee-search-item-result__item')
        for product in products:
            href = product.css('a::attr(href)').get()  # Lấy đường dẫn từng sản phẩm
            if href:
                product_url = response.urljoin(href)
                yield SeleniumRequest(
                    url=product_url,
                    wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '.WBVL_7 span')),
                    callback=self.parse_page
                )

    def parse_page(self, response):
        # Trích xuất dữ liệu từ trang chi tiết sản phẩm
        yield {
            'product_name': response.css('.WBVL_7 span::text').get(),
            'product_price': response.css('.B67UQ0::text').get(),
        }

