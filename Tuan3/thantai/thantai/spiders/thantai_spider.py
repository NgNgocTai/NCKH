import scrapy
from ..items import ThantaiItem
from datetime import datetime, timedelta

class ThantaiSpider(scrapy.Spider):
    name = "thantai_spider"
    allowed_domains = ["www.thantai1.net"]
    
    start_date = "12-11-2024"
    end_date = "12-01-2025"
    
    # Cộng ngày
    def add_days(self, start_date, days_to_add):
        current_date = datetime.strptime(start_date, "%d-%m-%Y")
        new_date = current_date + timedelta(days=days_to_add)
        return new_date.strftime("%d-%m-%Y")

    def start_requests(self):
        # Tạo URL từ ngày trong `self.start_date`
        url = f"https://www.thantai1.net/xo-so-truyen-thong/{self.start_date}"
        
        # Tạo yêu cầu và trả về cho Scrapy để xử lý
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Lấy kết quả giải đặc biệt
        special_prize = response.css(".text-danger::text").get()

        # Trả về dữ liệu dưới dạng item
        yield {
            "special_prize": special_prize,
            "date": self.start_date
        }

        start_date_obj = datetime.strptime(self.start_date, "%d-%m-%Y")
        end_date_obj = datetime.strptime(self.end_date, "%d-%m-%Y")
        if start_date_obj < end_date_obj:
            self.start_date = self.add_days(self.start_date, 1)
            # Tạo URL mới cho ngày tiếp theo và gửi yêu cầu
            next_url = f"https://www.thantai1.net/xo-so-truyen-thong/{self.start_date}"
            yield scrapy.Request(next_url, callback=self.parse)
