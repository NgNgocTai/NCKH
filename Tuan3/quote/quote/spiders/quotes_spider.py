# .\venv\Scripts\activate


# import scrapy
# from ..items import QuoteItem

# class QuoteSpider(scrapy.Spider):
#   name = 'quotes'
#   start_urls = ["https://quotes.toscrape.com/"]
  
#   def parse(self,response) :
#     div_quote = response.css('div.quote')
    
#     for quote in div_quote :
#       item = QuoteItem()
#       item['title'] =quote.css('span.text::text').extract()
#       item['author'] = quote.css('.author::text').extract()
#       item['tags'] = quote.css('.tag::text').extract() 
#       yield item 

import scrapy
import time
from ..items import QuoteItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ["https://quotes.toscrape.com/"]
    
    def __init__(self):
        # Ghi nhận thời gian bắt đầu
        self.start_time = time.time()
    
    def parse(self, response):
        div_quote = response.css('div.quote')
        
        for quote in div_quote:
            item = QuoteItem()
            item['title'] = quote.css('span.text::text').extract()
            item['author'] = quote.css('.author::text').extract()
            item['tags'] = quote.css('.tag::text').extract() 
            yield item
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def closed(self, reason):
        end_time = time.time()
        total_time = end_time - self.start_time
        total_quotes = self.crawler.stats.get('item_scraped_count', 0)
        
        self.logger.info(f"⏱️ Thời gian chạy Scrapy: {total_time:.2f} giây")
        self.logger.info(f"📊 Tổng số quote thu thập được: {total_quotes}")


