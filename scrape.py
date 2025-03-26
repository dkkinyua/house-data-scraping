import re
import json
import time
import requests
from bs4 import BeautifulSoup

properties = []
titles = []
locations = []
prices = []

url_pages = [x for x in range(2, 135)]

for x in url_pages:
    url = f'https://www.buyrentkenya.com/houses-for-sale?page={x}'

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try: 
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        title_elements = soup.find_all('span', class_='relative top-[2px] hidden md:inline')
        
        for title in title_elements:
            title_text = title.get_text(strip=True)
            titles.append(title_text)
            # print(title_text)

        location_elements = soup.find_all('p', class_='ml-1 truncate text-sm font-normal capitalize text-grey-650')

        for location in location_elements:
            location_text = location.get_text(strip=True)
            locations.append(location_text)

        price_elements = soup.find_all('a', class_='no-underline')
        all_text = " ".join([element.get_text(strip=True) for element in price_elements])

        found_prices = re.findall(r'KSh\s[\d,]+', all_text)
        prices.extend([price.replace("KSh", "").strip() for price in found_prices])
       # print(found_prices)

        time.sleep(response.elapsed.total_seconds()) # Make another request after the time spend to make the last request. 
    except Exception as e:
        print(f'Error: {str(e)}')

print(f'{len(titles)} titles scrapped successfully!')

#title_text = [i.text.strip() if i else "No Title" for i in title]

#location = soup.find_all('p', class_='ml-1 truncate text-sm font-normal capitalize text-grey-650')
#location_text = [x.text.strip() if x else 'No Location' for x in location]
# print(location_text)

#price = soup.find_all('a', class_='no-underline')
#price_text = [i.text.strip() for i in price if re.match(r'KSh \d{1,3}(?:,\d{3})*(?:\.\d+)?|Price not communicated', i.text.strip())]






