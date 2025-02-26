from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def setup_driver():
    # Khởi tạo trình điều khiển Chrome
    service = Service(r"D:\Code\NCKH\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.marksandspencer.com/denim-maxi-skirt/p/clp60721306')
    return driver

def accept_cookies(driver):
    # Chờ nút chấp nhận cookie xuất hiện và nhấp vào
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ot-sdk-row")))
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

def get_basic_info(driver):
    # Lấy thông tin cơ bản của sản phẩm
    brand = driver.find_element(By.CLASS_NAME, "brand-title_title__u6Xx5").text
    title = driver.find_element(By.TAG_NAME, "h1").text
    price = driver.find_element(By.CSS_SELECTOR, ".product-intro_priceWrapper__XRTSR .media-0_headingSm__aysOm").text
    product_code = driver.find_element(By.XPATH, "//*[(@id = 'product-info')]//*[contains(concat(' ', @class, ' '), ' media-0_textXs__ZzHWu ')]").text
    description = driver.find_element(By.CSS_SELECTOR, "#product-info .eco-box_mb__SXq72 .media-0_textSm__Q52Mz+ .media-0_textSm__Q52Mz").text
    return brand, title, price, product_code, description

def extract_text(elements):
    # Trích xuất nội dung văn bản từ danh sách phần tử
    return [el.text for el in elements]

def get_details_and_care(driver):
    # Lấy thông tin chi tiết và hướng dẫn bảo quản sản phẩm
    box = driver.find_element(By.CLASS_NAME, "accordion_body__sPtbq")
    divs = box.find_elements(By.CLASS_NAME, "eco-box_mb__SXq72")
    composition = box.find_element(By.CLASS_NAME, "product-details_compositionContainer__41Y7n")

    # Mở phần tử chứa thông tin chi tiết nếu chưa mở
    details_section = driver.find_element(By.ID, "accordion-Details-&-care")
    if not details_section.get_attribute("open"):
        driver.execute_script("arguments[0].setAttribute('open', 'true')", details_section)
        time.sleep(2)

    return {
        "Item details": extract_text(divs[0].find_elements(By.CSS_SELECTOR, ".media-0_body__yf6Z_.product-details_dimension__nPlAW")),
        "Fit and style": extract_text(divs[1].find_elements(By.CSS_SELECTOR, ".media-0_body__yf6Z_.product-details_dimension__nPlAW")),
        "Composition": extract_text(composition.find_elements(By.CSS_SELECTOR, ".media-0_strong__aXigV + .media-0_body__yf6Z_")),
        "Care": extract_text(divs[2].find_elements(By.CSS_SELECTOR, ".media-0_body__yf6Z_.product-details_careText__48dt5"))
    }

def get_colors_and_sizes(driver):
    # Lấy danh sách màu sắc và kích thước của sản phẩm
    information = []
    ul_buttons = driver.find_elements(By.CLASS_NAME, "colour-swatch-list_item__01k86")
    for li in ul_buttons:
        li.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "selected-colour-option-text")))
        time.sleep(2)
        
        color = driver.find_element(By.ID, "selected-colour-option-text").text
        images = [img.get_attribute("src") for img in driver.find_elements(By.CSS_SELECTOR, "#sticky-header-after img")]
        
        size = {}
        labels = driver.find_elements(By.CLASS_NAME, "selector-group-array_header___IhU6")
        size_options = driver.find_elements(By.CLASS_NAME, "selector-group-array_array__hAWxQ")
        
        # Lấy thông tin kích thước theo từng danh mục
        for i in range(len(labels)):
            label = labels[i].text
            list_size_num = [li.find_element(By.TAG_NAME, "span").text for li in size_options[i].find_elements(By.TAG_NAME, "li")]
            size[label] = list_size_num
        
        information.append({"images": images, "color": color, "size": size})
    return information

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

def save_to_json(data, filename='product_info.json'):
    # Lưu dữ liệu vào file JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    # Chạy chương trình chính
    driver = setup_driver()
    accept_cookies(driver)
    
    # Lấy thông tin sản phẩm
    brand, title, price, product_code, description = get_basic_info(driver)
    details = get_details_and_care(driver)
    information = get_colors_and_sizes(driver)
    
    # Lấy thông tin outfits
    outfits = extract_outfits(driver)
    
    # Tạo dictionary chứa thông tin sản phẩm và outfits
    product_info = {
        "brand": brand,
        "title": title,
        "price": price,
        "product_code": product_code,
        "description": description,
        "information": information,
        "details&care": details,
        "outfits": outfits
    }
    
    save_to_json(product_info)
    print("Dữ liệu đã được lưu vào file product_info.json")
    driver.quit()

if __name__ == "__main__":
    main()
