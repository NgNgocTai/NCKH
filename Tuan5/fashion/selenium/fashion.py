from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Đường dẫn đầy đủ đến chromedriver.exe
service = Service(r"D:\Code\NCKH\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get('https://www.marksandspencer.com/denim-maxi-skirt/p/clp60721306')

# Đợi cookie load xong
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ot-sdk-row")))
accept_cookies = driver.find_element(By.ID, "onetrust-accept-btn-handler")
accept_cookies.click()

# Lấy thông tin
# Lấy thông tin thương hiệu (brand)
brand = driver.find_element(By.CLASS_NAME, "brand-title_title__u6Xx5").text
# Lấy tiêu đề (title)
title = driver.find_element(By.TAG_NAME, "h1").text
# Lấy giá tiền
price = driver.find_element(By.CLASS_NAME, "product-intro_priceWrapper__XRTSR .media-0_headingSm__aysOm").text
print(f"Brand: {brand}")
print(f"Title: {title}")
print(f"Price: {price}")
productCode = driver.find_element(By.XPATH, "//*[(@id = 'product-info')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'media-0_textXs__ZzHWu', ' ' ))]").text
print(productCode)

description = driver.find_element(By.CSS_SELECTOR, "#product-info .eco-box_mb__SXq72 .media-0_textSm__Q52Mz+ .media-0_textSm__Q52Mz").text
print(description)


# Tìm tất cả các <div> trong phần tử .accordion_body__sPtbq đầu tiên
box = driver.find_element(By.CLASS_NAME,"accordion_body__sPtbq")
divs = box.find_elements(By.CLASS_NAME, "eco-box_mb__SXq72")
composition = box.find_element(By.CLASS_NAME, "product-details_compositionContainer__41Y7n")

# Hàm hỗ trợ để lấy văn bản từ danh sách phần tử
def extract_text(elements):
    return [el.text for el in elements]

# Mở phần "Details & Care" nếu chưa mở
details_section = driver.find_element(By.ID, "accordion-Details-&-care")
if not details_section.get_attribute("open"):
    driver.execute_script("arguments[0].setAttribute('open', 'true')", details_section)
    time.sleep(2)  # Đợi nội dung load sau khi mở
# Lấy văn bản từng phần
item_details = extract_text(WebDriverWait(divs[0], 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".media-0_body__yf6Z_.product-details_dimension__nPlAW"))))
fit_and_style = extract_text(WebDriverWait(divs[1], 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".media-0_body__yf6Z_.product-details_dimension__nPlAW"))))
composition_text = extract_text(WebDriverWait(composition, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".media-0_strong__aXigV + .media-0_body__yf6Z_"))))
care = extract_text(WebDriverWait(divs[2], 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".media-0_body__yf6Z_.product-details_careText__48dt5"))))

# Định dạng dữ liệu thành JSON
details = {
    "Item details": item_details,
    "Fit and style": fit_and_style,
    "Composition": composition_text,
    "Care": care
}

# print(details)

# waysToStyle = driver.find_element(By.CSS_SELECTOR,".pdp-outfits-carousel_pdpOutfitsCarouselWrapper__F7sY3 .carousel_root__bmbkv")
# ways = waysToStyle.find_elements(By.CLASS_NAME,"outfit-card_cardLink__hcOTj")
# print(f"Ways:{len(ways)}")
# for way in ways:
#     try:
#         way.click()
#         print(f"✔ CLICK")
#         # Chờ popup hiển thị
#         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "modal_modalContent__vI854")))
#         # Lấy các thông tin ở trong
#         box_infor = driver.find_element(By.CLASS_NAME,"modal_modalContent__vI854")
#         # Lấy ra tiêu đề (VD: Shop the outfit)
#         titles = box_infor.find_elements(By.CLASS_NAME,"carousel_header__948V7")
#         #Lấy ra các chập ảnh
#         contents = box_infor.find_elements(By.CSS_SELECTOR, "ul.eco-box_ecoBox__50nux.eco-box_gap__B80YD.eco-box_gapPolyfill__zyYBi.listUnstyled.carousel_slides__n_k7Q")

#         outfits =[]
#         #DUYỆT TỪNG CỤC MỘT
#         for i in range(len(titles)):
#             title = titles[i].find_element(By.TAG_NAME,"p").text
#             lis = contents[i].find_elements(By.TAG_NAME,"li")
#             links =[]
#             for li in lis:
#                 img = li.find_element(By.TAG_NAME,"img")
#                 link = img.get_attribute("src")  # Lấy đường dẫn ảnh
#                 links.append(link)
#             # Thêm vào danh sách outfits dưới dạng một object (dict)
#             # //Không biết nên để dạng như này hay là outfits[title]=links
#             outfits.append({
#                 "title": title,
#                 "links": links
#             })            
#             print(f"title: {title}")
#             print(f"links:{links}")  # In danh sách các link ảnh để kiểm tra
#         print(f"NICE: {len(titles)}, {len(contents)}")
        
#         # # Chờ popup hiển thị
#         # WebDriverWait(driver, 5).until(
#         #     EC.presence_of_element_located((By.CLASS_NAME, "modal_modalContent__vI854"))
#         # )
#         # popup = driver.find_element(By.CLASS_NAME, "modal_modalContent__vI854")
#         # time.sleep(1)  # Chờ một chút để trình duyệt cập nhật giao diện

#         # button = popup.find_element(By.CLASS_NAME,"modal_modalCloseButton__8qzIY")
#         # button.click()
#         # print("✔ Đã đóng popup")

#     except Exception as e:
#         break
#         print(f"❌ Lỗi outfit:{e}")

information = []
ul_buttons = driver.find_elements(By.CLASS_NAME, "colour-swatch-list_item__01k86")
print(f"Số lượng màu sắc tìm thấy: {len(ul_buttons)}")
for li in ul_buttons:
    li.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "selected-colour-option-text")))
    time.sleep(2)
    
    # Lấy màu sắc
    color = driver.find_element(By.ID, "selected-colour-option-text").text
    print(color)
    # Lấy tất cả ảnh trong phần tử có ID 'sticky-header-after'
    images = driver.find_elements(By.CSS_SELECTOR, "#sticky-header-after img")
    links = []
    # Lặp qua từng ảnh và lấy đường dẫn
    for img in images:
       link = img.get_attribute("src")
       links.append(link)

    # Lấy size
    size = {}
    labels = driver.find_elements(By.CLASS_NAME, "selector-group-array_header___IhU6")
    sizeOptions = driver.find_elements(By.CLASS_NAME, "selector-group-array_array__hAWxQ")
    
    # Duyệt từng nhãn và size
    for i in range(len(labels)):
    # Lấy ra nhãn
        label = labels[i].text
    # Lấy ra các size
        list_sizeNum = []
        sizeOption = sizeOptions[i]

    # Lấy ra list các li
        lis = sizeOption.find_elements(By.TAG_NAME, "li")
        for li in lis:
            size_num = li.find_element(By.TAG_NAME, "span").text
            list_sizeNum.append(size_num)
        
        size[label] = list_sizeNum
    
    # Thêm thông tin màu và kích thước vào danh sách thông tin
    information.append({"images":links,"color": color, "size": size})

# Tạo đối tượng chứa các thông tin cần lưu vào JSON
product_info = {
    "brand": brand,
    "title": title,
    "price": price,
    "information": information,
    "details&care":details
}

# Lưu thông tin vào file JSON
with open('product_info.json', 'w', encoding='utf-8') as f:
    json.dump(product_info, f, ensure_ascii=False, indent=4)

print("Dữ liệu đã được lưu vào file product_info.json")

# Đóng trình duyệt
driver.quit()
