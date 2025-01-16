import scrapy
from ..items import BookItem

class BookSpider(scrapy.Spider):
    name = "bookSpider"
    start_urls = ["http://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        # Lấy danh sách sách trên trang
        books = response.css('.product_pod')
        for book in books:
            href = book.css('a::attr(href)').get()  # Lấy link sách
            if href:
                yield response.follow(href, callback=self.parse_book)

        # Điều hướng tới trang tiếp theo
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        item = BookItem()
        # Trích xuất thông tin sách
        item['title'] = response.css('h1::text').get()
        item['price'] = response.css('.price_color::text').get()
        item['description'] = response.css('#product_description + p::text').get()
        item['upc'] = response.css('tr:nth-child(1) td::text').get()
        item['type_'] = response.css('tr:nth-child(2) td::text').get()
        item['tax'] = response.css('tr:nth-child(5) td::text').get()
        item['stock'] = response.css('tr:nth-child(6) td::text').get()
        item['reviews'] = response.css('tr:nth-child(7) td::text').get()
        yield item
