import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# QuotetoScrape

# Khởi tạo thời gian bắt đầu
start_time = time.time()

# Đường dẫn đầy đủ đến chromedriver.exe
service = Service(r"D:\Code\NCKH\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Danh sách lưu kết quả
quotes = []

# Mở trang web
driver.get("https://quotes.toscrape.com/")

while True:
    # Đợi các quote load xong
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "quote"))
    )
    
    div_quotes = driver.find_elements(By.CLASS_NAME, "quote")
    
    for quote in div_quotes:
        title = quote.find_element(By.CSS_SELECTOR, "span.text").text
        author = quote.find_element(By.CSS_SELECTOR, ".author").text
        tags = [tag.text for tag in quote.find_elements(By.CSS_SELECTOR, ".tag")]
        
        quotes.append({
            "title": title,
            "author": author,
            "tags": tags
        })
    
    # Kiểm tra nút "Next" để chuyển trang
    next_buttons = driver.find_elements(By.CSS_SELECTOR, "li.next a")
    if next_buttons:
        next_buttons[0].click()
    else:
        break

# Đóng trình duyệt
driver.quit()

# Tính thời gian chạy
end_time = time.time()
total_time = end_time - start_time
print(f"⏱️ Thời gian chạy Selenium: {total_time:.2f} giây")
print(f"📊 Tổng số quote thu thập được: {len(quotes)}")

# Lưu dữ liệu vào file JSON
output_file = "quotes.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(quotes, f, indent=4, ensure_ascii=False)

print(f"Dữ liệu đã được lưu vào file {output_file}")

# In một số quote để kiểm tra
for q in quotes[:5]:
    print(q)
