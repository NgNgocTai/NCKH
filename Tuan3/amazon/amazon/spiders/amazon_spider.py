#.\venv\Scripts\activate
import scrapy
from ..items import AmazonItem

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = ["https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&qid=1736357386&xpid=JvLIogjQ33vol&ref=sr_pg_1"]
    page_number = 2
    def parse(self, response):
        item = AmazonItem()
        books = response.css(".s-main-slot .s-result-item")
        for book in books:
            item["title"] = book.css(".a-color-base.a-text-normal span").css("::text").get()
            item["author"]=book.css(".a-color-secondary .a-row .a-size-base+ .a-size-base , .a-color-secondary .a-size-base.s-link-style").css("::text").get()
            item["price"]=book.css(".puis-price-instructions-style .a-text-normal > .a-price span").css("::text").get()
            item["img"] = book.css(".s-image::attr(src)").get()
            if( item["title"] is not None):
                yield item
            next_page = "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&qid=1736357386&xpid=JvLIogjQ33vol&ref=sr_pg_" + str(AmazonSpider.page_number)
            if(AmazonSpider.page_number<=400):
                AmazonSpider.page_number+=1
                yield response.follow(next_page, callback=self.parse)
            
            
