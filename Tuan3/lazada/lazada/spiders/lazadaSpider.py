import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
class LazadaSpider(scrapy.Spider):
    name = 'lazada'
    allowed_domains = ['lazada.co.id']
    start_urls = ['http://lazada.co.id/']

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.lazada.co.id/catalog/?spm=a2o4j.searchlist.0.0.3d1dcc88pVX60h&from=input&q=laptop&page=1",
            wait_time=10,
            callback=self.parse,
        )

    def parse(self, response):
        print(response.text)
        product_name = response.css('div._17mcb > div:nth-child(1) > div > div > div.buTCk > div.RfADt > a::text').extract_first()
        product_price = response.css('.ooOxS::text').extract_first()
        if product_name:
            print(product_name)
        else:
            print("Không tìm thấy tên sản phẩm")

        if product_price:
            print(product_price)
        else:
            print("Không tìm thấy tên giá")