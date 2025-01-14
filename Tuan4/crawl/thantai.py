from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
from datetime import datetime, timedelta
service = Service(executable_path="Tuan4/chromedriver.exe")
driver = webdriver.Chrome(service=service)

 #Cộng ngày
def add_days(start_date, days_to_add):
    current_date = datetime.strptime(start_date, "%d-%m-%Y")
    new_date = current_date + timedelta(days=days_to_add)
    return new_date.strftime("%d-%m-%Y")

start_day = "12-11-2024"
end_day = "12-01-2025"
end_day = add_days(end_day,1)

# Danh sách lưu kết quả
results = []
while(start_day!=end_day):
  driver.get("https://www.thantai1.net/xo-so-truyen-thong/" + start_day)
  WebDriverWait(driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR,".text-danger")))
  special_prize = driver.find_element(By.CSS_SELECTOR,".text-danger")
  
   # Lưu kết quả vào danh sách
  result = {"date": start_day, "special_prize": special_prize.text}
  results.append(result)
   # Tăng ngày lên 1
  start_day = add_days(start_day,1)
  
# Ghi kết quả vào tệp JSON
with open("results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=4)
time.sleep(10)

