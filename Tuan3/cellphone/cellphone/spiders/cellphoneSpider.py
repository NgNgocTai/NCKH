import scrapy
class CellphoneSpider(scrapy.Spider):
    name = "cellphones"
    start_urls = ["https://cellphones.com.vn/laptop/mac.html"]

    def parse(self, response):
        # Duyệt qua từng sản phẩm
        laptops = response.css('.product-item')
        for laptop in laptops:
            # Trích xuất link của sản phẩm
            laptop_link = laptop.css('a::attr(href)').get()
            if laptop_link:
                # Điều hướng đến trang chi tiết sản phẩm
                yield response.follow(laptop_link, self.parse_laptop)

    def parse_laptop(self, response):
        # Trích xuất các tính năng nổi bật
        key_feature = response.css('.box-ksp div')
        product_feature = [];
        # Lấy key từ thẻ <p>
        key = key_feature.css('p.desktop::text').get()
        # Lấy danh sách các value từ <li>
        values = key_feature.css('ul li::text').getall()
        if key and values:
            product_feature = values

        # Trích xuất thông tin sản phẩm
        product_infor = []
        infor_title = response.css('.box-title p::text').get()
        infor_values = response.css('.description::text').getall()
        if infor_title and infor_values:
            product_infor= infor_values
            
        # Trích xuất thông tin cấu hình
        configurations = []
        configuration_items = response.css('.list-linked a')
        for item in configuration_items:
            # Trích xuất thông tin từng cấu hình
            configuration_cpu_gpu = item.css('strong:nth-of-type(1)::text').get(default="").strip()
            configuration_memory = item.css('strong:nth-of-type(2)::text').get(default="").strip()
            price = item.css('span::text').get(default="").strip()
            link = item.css('::attr(href)').get(default="").strip()

            # Kiểm tra và thêm dữ liệu vào danh sách configurations
            if configuration_cpu_gpu and configuration_memory and price:
                configurations.append({
                    "configuration": f"{configuration_cpu_gpu}, {configuration_memory}",
                    "price": price,
                    "link": response.urljoin(link)  # Tạo link đầy đủ
                })
        #C1
        colors = []
        ul_colors = response.css('.list-variants li')
        for li_color in ul_colors:
            color = ul_colors.css('.item-variant-name::text').get()
            price = ul_colors.css('.item-variant-price::text').get()
            if color and price:
                colors.append({
                    "color": color.strip(),
                    "price": price.strip()
                })
                
        #C2    
        # Khởi tạo dictionary để lưu dữ liệu
        # colors = {}
        # # Lấy danh sách các màu sắc và giá tương ứng
        # ul_colors = response.css('.list-variants li')
        # for li_color in ul_colors:
        #     color = li_color.css('.item-variant-name::text').get()
        #     price = li_color.css('.item-variant-price::text').get()
        #     if color and price:
        #         # Thêm vào dictionary, dùng color làm key và price làm value
        #         colors[color.strip()] = price.strip()
        
        # Khởi tạo danh sách chứa thông số kỹ thuật
        technical_spec = []
        # Lấy danh sách các phần tử trong technical-content
        technical_content = response.css('.technical-content li')
        
        for tech in technical_content:
            key = tech.css('p::text').get()  
            value = tech.css('div::text').get()

            # Kiểm tra nếu cả key và value đều không None
            if key and value:
                technical_spec.append({
                    key: value
                })
        yield {
            "features": product_feature,
            "information": product_infor,
            "configurations": configurations,
            "colors":colors,
            "technical_spec": technical_spec
        }
  #  # Trích xuất thông tin thành phố và cửa hàng
        # city = {}
        # city_name =response.css('.button__change-province::text').get()
        # shops = response.css('.box-on-stock-address')
        # values = []
        # for shop in shops:
        #     shop_phone = shop.css('.phone a::text').get(default="").strip()
        #     shop_address = shop.css('.address::attr(title)').get(default="").strip()
        #     if shop_phone and shop_address:
        #         shop_infor = f"{shop_phone} - {shop_address}"
        #         values.append(shop_infor)
        # if city_name and values:
        #     city[city_name.strip()] = values