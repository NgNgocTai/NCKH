# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def setup_driver():
#     service = Service(r"D:\Code\NCKH\chromedriver.exe")
#     driver = webdriver.Chrome(service=service)
#     driver.get('https://www.marksandspencer.com/denim-maxi-skirt/p/clp60721306')
#     return driver

# def accept_cookies(driver):
#     WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ot-sdk-row")))
#     driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    
# def click_nextButton(ways_to_style, driver):
#     next_button = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((By.CLASS_NAME, "pagination_trigger__YEwyN"))
#     )
#     driver.execute_script("arguments[0].scrollIntoView();", next_button)  # Cuộn xuống trước
#     time.sleep(1)  # Chờ 1 chút

# def extract_outfits(driver):
#     try:
#         ways_to_style = driver.find_element(By.CSS_SELECTOR, ".pdp-outfits-carousel_pdpOutfitsCarouselWrapper__F7sY3 .carousel_root__bmbkv")
#         ways = ways_to_style.find_elements(By.CLASS_NAME, "outfit-card_cardLink__hcOTj")
        
#         outfits = []
#         for way in ways:
#             try:
#                 if not way.is_displayed() or not way.is_enabled():
#                     print("🔄 Way bị che, nhấn nút Next trước...")
#                     click_nextButton(ways_to_style, driver)  # Nhấn nút "Next"
#                     time.sleep(1)  # Đợi trang cập nhật
                
#                 way.click()
#                 WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "modal_modalContent__vI854")))
#                 box_info = driver.find_element(By.CLASS_NAME, "modal_modalContent__vI854")
                
#                 titles = box_info.find_elements(By.CLASS_NAME, "carousel_header__948V7")
#                 contents = box_info.find_elements(By.CSS_SELECTOR, "ul.eco-box_ecoBox__50nux.eco-box_gap__B80YD.eco-box_gapPolyfill__zyYBi.listUnstyled.carousel_slides__n_k7Q")
                
#                 for i in range(len(titles)):
#                     title = titles[i].find_element(By.TAG_NAME, "p").text
#                     lis = contents[i].find_elements(By.TAG_NAME, "li")
#                     links = [li.find_element(By.TAG_NAME, "img").get_attribute("src") for li in lis]
#                     outfits.append({"title": title, "links": links})
                    
#                 close_button = driver.find_element(By.CLASS_NAME, "modal_modalCloseButton__8qzIY")
#                 close_button.click()
#                 time.sleep(1)
#             except Exception as e:
#                 print(f"❌ Lỗi outfit: {e}")
#                 time.sleep(2)
#                 continue
        
#         return outfits
#     except Exception as e:
#         print(f"❌ Không thể lấy outfit: {e}")
#         return []



# def save_to_json(data, filename):
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

# def main():
#     driver = setup_driver()
#     accept_cookies(driver)
#     outfits = extract_outfits(driver)
#     save_to_json(outfits, 'outfits_info.json')
#     print("Dữ liệu outfit đã được lưu vào file outfits_info.json")
#     driver.quit()

# if __name__ == "__main__":
#     main()
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    service = Service(r"D:\Code\NCKH\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.marksandspencer.com/denim-maxi-skirt/p/clp60721306')
    return driver

def accept_cookies(driver):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ot-sdk-row")))
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    
def click_nextButton(ways_to_style, driver):
    next_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "pagination_trigger__YEwyN"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", next_button)  # Cuộn xuống trước
    time.sleep(1)  # Chờ 1 chút
    next_button.click()

def extract_outfits(driver):
    try:
        ways_to_style = driver.find_element(By.CSS_SELECTOR, ".pdp-outfits-carousel_pdpOutfitsCarouselWrapper__F7sY3 .carousel_root__bmbkv")
        ways = ways_to_style.find_elements(By.CLASS_NAME, "outfit-card_cardLink__hcOTj")
        
        outfits = []
        for way in ways:
            try:
                if not way.is_displayed() or not way.is_enabled():
                    print("🔄 Way bị che, nhấn nút Next trước...")
                    click_nextButton(ways_to_style, driver)  # Nhấn nút "Next"
                    time.sleep(1)  # Đợi trang cập nhật
                
                driver.execute_script("arguments[0].scrollIntoView();", way)
                time.sleep(1)
                way.click()
                
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "modal_modalContent__vI854")))
                box_info = driver.find_element(By.CLASS_NAME, "modal_modalContent__vI854")
                
                titles = box_info.find_elements(By.CLASS_NAME, "carousel_header__948V7")
                contents = box_info.find_elements(By.CSS_SELECTOR, "ul.eco-box_ecoBox__50nux.eco-box_gap__B80YD.eco-box_gapPolyfill__zyYBi.listUnstyled.carousel_slides__n_k7Q")
                
                for i in range(len(titles)):
                    title = titles[i].find_element(By.TAG_NAME, "p").text
                    lis = contents[i].find_elements(By.TAG_NAME, "li")
                    links = [li.find_element(By.TAG_NAME, "img").get_attribute("src") for li in lis]
                    outfits.append({"title": title, "links": links})
                    
                close_button = driver.find_element(By.CLASS_NAME, "modal_modalCloseButton__8qzIY")
                close_button.click()
                time.sleep(1)
            except Exception as e:
                print(f"❌ Lỗi outfit: {e}")
                time.sleep(2)
                continue
        
        return outfits
    except Exception as e:
        print(f"❌ Không thể lấy outfit: {e}")
        return []

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    driver = setup_driver()
    accept_cookies(driver)
    outfits = extract_outfits(driver)
    save_to_json(outfits, 'outfits_info.json')
    print("Dữ liệu outfit đã được lưu vào file outfits_info.json")
    driver.quit()

if __name__ == "__main__":
    main()
