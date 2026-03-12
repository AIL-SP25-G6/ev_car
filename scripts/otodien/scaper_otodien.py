# data được lấy từ trang "https://otodien.vn"

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime,timedelta
import re

BASE_URL = "https://otodien.vn"
LISTING_URL = "https://otodien.vn/mua-ban-oto-dien"
CSV_FILE = "data_xe_dien.csv"

HEADERS = ['ID', 'Tên', 'Tiền (VNĐ)', "Vị trí", 'Ngày đăng', 'Người dùng','Sao','Đã bán', 'Đang bán',
           'Thông tin mô tả', 'Tính năng nổi bật', 'Tính năng khác',
           'Kiểu dáng', 'Màu bên ngoài', 'Chiều dài(mm)', 'Chiều dài cơ sở(mm)', 'Chiều rộng(mm)',
           'khoảng sáng gầm(mm)', 'Số chỗ ngồi', 'Trọng lượng bản thân (kg)', 'Trọng lượng toàn tải (kg)',
           'Dung tích khoang hành lý (lít)', 'Dung tích khoang hành lý khi gập ghế sau (lít)',
           'Công suất tốt đa(hp)', 'Tốc độ tối đa (km/h)', '0-100(s)', 'Tầm hoạt động (km)',
           'Dung lượng pin (kWh)','Chi phí sạc đầy (VNĐ)', 'Chi phí sạc hàng tháng (VNĐ)', 'Sạc chậm (giờ)',
           'Sạc tiêu chuẩn (giờ)', 'Phần trăm sạc treo tường', 'phút sạc treo tường']

REQ_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def tinh_ngay_dang(chuoi_thoi_gian):
    thoi_gian_hien_tai = datetime.now()

    match = re.search(r'(\d+)\s+(giây|phút|giờ|tiếng|ngày|tuần|tháng|năm)', chuoi_thoi_gian.lower())

    if not match:
        return None

    so_luong = int(match.group(1))
    don_vi = match.group(2)

    if don_vi == 'giây':
        delta = timedelta(seconds=so_luong)
    elif don_vi == 'phút':
        delta = timedelta(minutes=so_luong)
    elif don_vi in ['giờ', 'tiếng']:
        delta = timedelta(hours=so_luong)
    elif don_vi == 'ngày':
        delta = timedelta(days=so_luong)
    elif don_vi == 'tuần':
        delta = timedelta(weeks=so_luong)
    elif don_vi == 'tháng':
        delta = timedelta(days=so_luong * 30)
    elif don_vi == 'năm':
        delta = timedelta(days=so_luong * 365)
    else:
        return None

    ngay_dang = thoi_gian_hien_tai - delta
    return ngay_dang.date()

def get_car_link(page_url):
    # print(f"Đang quét trang danh sách: {page_url}")
    response = requests.get(page_url, headers=REQ_HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    items = soup.select('.car-title a') 
    
    for item in items:
        href = item.get('href')
        if href:
            # Xử lý link tương đối. 
            # Trong ảnh của bạn, href là "/mua-ban-oto/100000779" (link tương đối)
            # Đoạn code này sẽ tự động ghép thêm "https://otodien.vn" vào trước
            full_link = href if href.startswith("http") else BASE_URL + '/' + href
            links.append(full_link)
        
    return list(set(links))

def extract_data(link: str):
    # print(f"cào trang: {link}")
    respose = requests.get(link, headers = REQ_HEADERS)
    soup = BeautifulSoup(respose.text, "html.parser")

    row = []

    #ID
    row.append(link)

    #name
    name_tag = soup.find('h1')
    row.append(str(name_tag.text.strip().split('-')[0] if name_tag else ""))

    #tiền, vị trí, thời gian đăng
    MoneyLocationTime = soup.find('div', class_ ='col-md-4 r6o4304')
    #tiền
    money_list = []
    transform = {'triệu':'000000', 'nghìn':'000', 'tỷ':'000000000'}
    money_tag = MoneyLocationTime.find('b', class_ = 'p26z2wb').text.strip().split()
    for index, i in enumerate(money_tag):
        if i in transform:
            money_list.append(int(money_tag[index-1]+ transform[i]))
    money = sum(money_list)
    row.append(str(money))

    #Vị trí
    location = MoneyLocationTime.find('span', class_ = "bwq0cbs flex-1")
    row.append(str(location.text.strip() if location else ""))

    #thời gian
    raw_text_time = MoneyLocationTime.find_all('span', class_ = 'bwq0cbs')[1]
    text_time = raw_text_time.text.strip()
    row.append(tinh_ngay_dang(text_time))

    #user
    raw_user_name = soup.find('div', class_ = 'pf9ruvz vdi4wk')
    user_name = raw_user_name.text.strip()
    row.append(user_name)

    #rating
    row.append(soup.find('b', class_ = 'seller-rating').text.strip('() '))

    #sold, selling
    ss = soup.find_all('span', class_ = 'bwq0cbs')[-2:]
    sold = ss[0].text.strip(' đã bán')
    selling = ss[1].text.strip(' đang bán')
    row.extend([sold, selling])

    #thông tin
    details = soup.find('div', class_ = "col-md-8 col-12")

    #Thông tin mô tả
    decription_tag = details.find('p', class_ = "cvatvjo")
    if decription_tag:
        #thay thế "\n" thành "-" và "\r" thành ""
        decription = decription_tag.text.strip().replace('\n', '-').replace('\r', '')
    else:
        decription = ""
    row.append(decription)

    #tính năng nổi bật
    highlights_tag = details.find_all('li', class_ = "row-3 otodien-feature-highlight")
    highlight_tag = [ item.text.strip() for item in highlights_tag]
    row.append(str(" - ".join(highlight_tag)))

    #tính năng khác
    features_tag = details.find_all('li', class_ = "row-3 otodien-feature")
    feature_tag = [ item.text.strip().replace("+ ", "") for item in features_tag]
    row.append(str(" - ".join(feature_tag)))

    # điều kiện loại text đằng sau
    condition = ["hp", "km/h", "giây","kWh", "VNĐ", "km", "phút", "giờ","Sạc đầy khoảng","dưới ", "%", "trong "]

    # ngoại, nội thất, hiệu suất
    NNH_tag = details.find("ul", class_="data-list-wrap cols-3 tablet-cols-3 mobile-cols-1")
    NNH_inner_tag = NNH_tag.find_all("span", class_="heading-font")
    for item in NNH_inner_tag:
        clean_item = item.text.strip().split(" ")
        if clean_item[-1] in condition:
            clean_item = clean_item[0]
        else:
            clean_item = " ".join(clean_item)
        row.append(str(clean_item.strip()))

    # sạc, sạc tại nhà
    SSNs_tag = details.find("ul", class_ = "data-list-wrap cols-2 tablet-cols-2 mobile-cols-1")
    SSN_inner_tag = SSNs_tag.find_all("span", class_ = "heading-font")
    for item in SSN_inner_tag:
        clean_item = item.text.strip()
        #xem text và thay thế
        for i in condition:
            if i in clean_item:
                clean_item = clean_item.replace(i, '')
        row.extend(clean_item.strip().split(" "))
    return row

# test
# print(extract_data("https://otodien.vn/mua-ban-oto/100000797"))

def main():
    # Mở file CSV để ghi dữ liệu. Dùng utf-8-sig để Excel không bị lỗi font tiếng Việt
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)

        car_links =[]
        for i in range(1,42):
        # 1. Lấy danh sách link
            car_links += get_car_link(LISTING_URL + f'?page={i}')
        print(f"Tìm thấy {len(car_links)} xe. Bắt đầu cào chi tiết...")

        for link in car_links:
                try:
                    car_data = extract_data(link)
                    writer.writerow(car_data)
                except Exception as e:
                    print(f"Lỗi khi cào link {link}: {e}")

    print(f"Hoàn thành! Dữ liệu đã được lưu vào file {CSV_FILE}")

if __name__ == "__main__":
    main()