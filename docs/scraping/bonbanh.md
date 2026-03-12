# Bonbanh Scraping Report

## 1. What is on the website
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

## 2. Libraries/Frameworks used
* `requests`: To send HTTP requests and manage sessions (maintaining cookies and headers).
* `BeautifulSoup` (from `bs4`): To parse HTML and extract specific elements using CSS selectors.
* `pandas`: To structure the scraped data into a DataFrame and export it to a clean, well-formatted CSV file.
* `re` (Regular Expression): To clean up messy text strings and extract specific patterns (like addresses or split titles).
* `time` & `random`: To pause the script randomly between requests, simulating human browsing behavior.

## 3. Script Structure (Main Functions)
* `get_value_exact(soup, label_name)`: A helper function to find specific vehicle specifications dynamically, handling different HTML class variations.
* `get_car_details(session, url)`: The core scraping function that visits a car's detail page and extracts all 19 required data points.
* `crawl_bonbanh_all_pages_final()`: The main controller that handles pagination, bypasses anti-scraping traps, collects all unique car links, and triggers the CSV export.


## 4. Scraping Logic

The script have 3 main functions:
* `get_value_exact`: use for scraping specific vehicle metrics and handling inconsistent HTML classes.
* `get_car_details`: use for scraping all necessary data from the details page.
* `crawl_bonbanh_all_pages_final` (main): use to control pagination, run all other functions, and export data to CSV.

Getting information:
* Getting details page url: use BeautifulSoup to find `li` with class `car-item` and get the `href` from the `a` tag.
* Name of the car and Price: use BeautifulSoup.find to get the `h1` tag, then use regex and `.rsplit("-")` to separate the car name and price.
* Time posted: use `div` with class `notes`, then use `.split()` and `.replace()` to remove text and get the exact date.
* Description: use `div` with class `des_txt` and get text using `separator=" | "` to merge multiple lines.
* Seller name: use `class_="cname"` to find the tag containing the seller's name.
* Seller address: use `div` with class `contact-txt` to get raw text, then use `re.search` (Regex) to extract the exact address and bypass hidden tags.
* Vehicle specifications: use `div` with classes `row` or `row_last` for the labels, and extract values from `txt_input` or `inputbox`.

### 5. Difficulties & Solutions
* **Infinite Pagination Loop:** * *Problem:* The site doesn't return a 404 error for non-existent pages. Instead, it reloads older listings, causing an endless scraping loop.  
  * *Solution:* Created a `seen_links` set to track scraped URLs. If a page yields 0 *new* links, the script realizes it's in a loop and automatically breaks out.
* **Anti-Crawling (IP Blocks):** * *Problem:* The server blocks IPs that send too many requests too quickly without a browser footprint.  
  * *Solution:* Used `requests.Session()` to keep cookies. Added standard browser `Headers` (User-Agent). Implemented `time.sleep(random.uniform(1.0, 2.0))` to simulate human reading time, and added a 3-retry mechanism for failed connections.
* **Inconsistent HTML Structures:** * *Problem:* Data fields didn't use the same CSS classes (e.g., some rows used `row`, others used `row_last`).  
  * *Solution:* Passed a list of possible classes into BeautifulSoup's find method (e.g., `class_=['row', 'row_last']`) to catch all variations.
* **Messy Text & Hidden Tags in Addresses:** * *Problem:* The contact block had hidden elements and random `<br>` tags, which cut off the address text prematurely.  
  * *Solution:* Extracted the whole block as raw text and used Regular Expressions (`Regex`) to strictly extract just the address string.