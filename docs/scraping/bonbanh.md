### 1. What is on the website
* **Main page:** A list of electric car listings with thumbnail images and brief summaries.
* **Details page:** The script extracts exactly 19 data points from each car's detail page, matching the structure of the exported CSV file:
  * Ngày đăng (Time posted)
  * Tên xe (Name of the car)
  * Giá (Price)
  * Tên người bán (Seller's name)
  * Địa chỉ (Seller's address)
  * Năm sản xuất (Year of manufacture)
  * Tình trạng (Condition)
  * Số Km đã đi (Mileage)
  * Xuất xứ (Origin)
  * Kiểu dáng (Body style)
  * Hộp số (Transmission)
  * Động cơ (Engine)
  * Màu ngoại thất (Exterior color)
  * Màu nội thất (Interior color)
  * Số chỗ ngồi (Number of seats)
  * Số cửa (Number of doors)
  * Dẫn động (Drivetrain)
  * Mô tả (Description of the car)
  * Link (URL of the listing)
  
### 2. Libraries/Frameworks used
* `requests`: To send HTTP requests and manage sessions (maintaining cookies and headers).
* `BeautifulSoup` (from `bs4`): To parse HTML and extract specific elements using CSS selectors.
* `pandas`: To structure the scraped data into a DataFrame and export it to a clean, well-formatted CSV file.
* `re` (Regular Expression): To clean up messy text strings and extract specific patterns (like addresses or split titles).
* `time` & `random`: To pause the script randomly between requests, simulating human browsing behavior.

### 3. Script Structure (Main Functions)
* `get_value_exact(soup, label_name)`: A helper function to find specific vehicle specifications dynamically, handling different HTML class variations.
* `get_car_details(session, url)`: The core scraping function that visits a car's detail page and extracts all 19 required data points.
* `crawl_bonbanh_all_pages_final()`: The main controller that handles pagination, bypasses anti-scraping traps, collects all unique car links, and triggers the CSV export.