# Scraper uses for website "bonbanh.com/oto-xe-dien"

### What is on the website:
* **Main page** contain a listing of electric cars and a brief description of each one.
* **Details page** of a car contain:
  * Name of the car.
  * Pricing.
  * Time posted (Ngày đăng).
  * Description of the car.
  * Sellers name.
  * Sellers address.
  * Vehicle specifications (Năm sản xuất, Tình trạng, Số Km đã đi, Xuất xứ, Kiểu dáng, Hộp số, Động cơ, Màu ngoại thất, Màu nội thất, Số chỗ ngồi, Số cửa, Dẫn động).

### Library/framework you used for the task
* `requests`
* `BeautifulSoup` from `bs4`
* `pandas`
* `re` (Regular Expression)
* `time`, `random`

### The script have 3 main functions:
* `get_value_exact`: use for scraping exact specification values from dynamic div structures (handling both normal and edge cases).
* `get_car_details`: use for scraping all necessary data (Name, Price, Address, Description, Specs) from the details page.
* `crawl_bonbanh_all_pages_final`: use to manage pagination, bypass anti-crawling mechanisms, control the flow, and export data to CSV.

### Getting information:
* **Getting details page url:** use BeautifulSoup to find `li` with class `car-item` and get the `href` for the url inside the `a` tag.
* **Name and Price:** use `h1` to get the full title. Use `re.sub` to normalize all dash characters, then use `.rsplit("-")` to separate the car's name and its price.
* **Time posted:** use `div` with class `notes`, then use string manipulation (`split` and `replace`) to extract the exact date.
* **Description:** use `div` with class `des_txt` and get text with `separator=" | "` to format multiple lines cleanly.
* **Sellers name:** use `class="cname"` to find the seller's name regardless of whether it uses an `<a>` tag (Showroom) or `<span>` tag (Individual).
* **Sellers address:** use `div` with class `contact-txt` to get raw text, then use Regular Expression `re.search(r'Địa chỉ\s*:\s*(.*?)(?:Website|Email|$)')` to extract the address cleanly bypassing hidden tags.
* **Vehicle specifications:** use `class_=['row', 'row_last']` to find the label, then extract the value from `class_=['txt_input', 'inputbox']` to handle inconsistent HTML structures.

### Difficulties
* **Infinite pagination loop:** The website returns old data on non-existent pages instead of a 404 error. 
  * *Resolved:* Used a `seen_links` set to track duplicates. If a page returns 0 new links, the script breaks the loop.
* **Anti-crawling (IP Blocking):** The server blocks IPs that send too many requests. 
  * *Resolved:* Implemented `requests.Session()`, added standard browser `Headers`, used `time.sleep(random.uniform())` for delays, and built a 3-retry mechanism.
* **Inconsistent HTML classes:** Specification rows end with different classes (`row` vs `row_last`, `txt_input` vs `inputbox`). 
  * *Resolved:* Passed a list of possible classes into BeautifulSoup's `find` method.
* **Messy text with hidden tags:** The seller's address block contains messy `<br>` and hidden elements causing standard text extraction to fail. 
  * *Resolved:* Used `Regex` on the raw text to strictly match the address string.