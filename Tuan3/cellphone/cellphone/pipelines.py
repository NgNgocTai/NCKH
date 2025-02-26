# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class CellphonePipeline:
    def process_item(self, item, spider):
        # Kiểm tra nếu item chứa thuộc tính 'information'
        if 'information' in item:
            # Làm sạch dữ liệu trong 'information'
            item['information'] = self.clean_data(item['information'])
        
        return item

    def clean_data(self, data):
        cleaned_data = []
        for item in data:
            item = item.strip()  # Loại bỏ khoảng trắng thừa từ đầu và cuối
            # Loại bỏ các dòng không chứa thông tin thực tế
            if not item or "Xem thông tin" in item or "CareS.vn" in item:
                continue
            cleaned_data.append(item)
        return cleaned_data
