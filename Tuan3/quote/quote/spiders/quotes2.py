import scrapy

class QuotesSpider2(scrapy.Spider):
  name = "quotes2"
  start_urls = [
    'http://quotes.toscrape.com/'
  ]
  
  def parse(self, response):
    all_quotes_div = response.css('div.quote')
    for quote in all_quotes_div :
      title = quote.css('span.text::text').extract()
      author = quote.css('small.author::text').extract()
      tags = quote.css('a.tag::text').extract()
      yield {
        'title': title,
        'author':author,
        'tags' :tags
      }
    