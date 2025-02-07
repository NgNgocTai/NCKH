from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# A game for fun

# Đường dẫn đầy đủ đến chromedriver.exe
service = Service(r"D:\Code\NCKH\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")

cookie_id = "bigCookie"
cookies_count_id = "cookies"
productName = "product"
productPrice= "productPrice"
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "langSelect-EN"))
)
language = driver.find_element(By.ID, "langSelect-EN")
language.click()
WebDriverWait(driver,5).until(
  EC.presence_of_element_located((By.ID,cookie_id))
)
cookie = driver.find_element(By.ID,cookie_id)


while True: 
  cookie.click()
  cookie_count = driver.find_element(By.ID,cookies_count_id).text.split(" ")[0].replace(",","")
  if cookie_count.isdigit():
    cookie_count = int(cookie_count)
  for i in range (4):
    product_price = driver.find_element(By.ID, productPrice + str(i)).text.replace(",", "")
    if product_price.isdigit():
        product_price = int(product_price)
    else:
        continue
    if cookie_count >=product_price:
      product_name = driver.find_element(By.ID, productName + str(i))
      product_name.click()
      break
time.sleep(10)

driver.close()