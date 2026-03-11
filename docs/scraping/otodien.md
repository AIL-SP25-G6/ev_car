# Scraper uses for website "https://otodien.vn/mua-ban-oto-dien"

## What is on the website:
- Main page contain a listing of cars and a brief description of each one
- Details page of a car contain:
  - Name of the car.
  - Pricing.
  - Description of the car.
  - The highlighted feature.
  - Others feature.
  - Vehicle specifications(outside, inside, vehicle performance). 
  - Battery details.
  - Sellers name, rating, sold cars, selling cars.
  - Sellers address.

## Library/framework you used for the task
- requests
- BeautifulSoup from bs4
- csv
- datetime,timedelta from datetime
- re

## scraping
The script have 4 main function:
- ___tinh_ngay_dang___: use for calculating the time of the post.
- ___get_car_link___: use for getting the details page from the main page.
- ___extract_data___: use for scraping the necessary data from the details page
- ___main___: use to control and run all the others function and code

## Getting information:
- **Getting details page url**:
  - use BeautifulSoup to find '.car-title a' and get the href for the url
- **name of the car**:
  - use BeautifulSoup.find to get the first 'h1' which contains the car name
- **price, location, time**:
  - use 'col-md-4 r6o4304' to find div that contain all 3 element
  - use 'p26z2wb' for price then a condition to change name currency to numbers
  - use 'bwq0cbs flex-1' for location
  - use the first 'bwq0cbs' for time
- **description**:
  - use 'col-md-8 col-12' and 'cvatvjo' for description
- **highlighted feature**:
  - use 'row-3 otodien-feature-highlight' for highlighted feature
- **Others feature**:
  - use 'row-3 otodien-feature' for the element
- **Vehicle specifications**:
  - use conditions to remove all unnecessary metrics(e.g. km/h, kWh,...)
  - use 'data-list-wrap cols-3 tablet-cols-3 mobile-cols-1' and 'data-list-wrap cols-2 tablet-cols-2 mobile-cols-1' for the element
- **Sellers name, rating, sold cars, selling cars**:
  - use 'pf9ruvz vdi4wk' div for seller name
  - use 'seller-rating' for rating
  - use the second 'bwq0cbs' for sold
  - use the third  'bwq0cbs' for selling
## Difficulties
None