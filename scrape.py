import re
import json
import time
import requests
from bs4 import BeautifulSoup

def scrape():
    properties = []
    titles = []
    locations = []
    prices = []

    base_url = 'https://www.buyrentkenya.com/houses-for-sale'
    url_pages = [base_url]

    url_pages.extend([f'{base_url}?page={x}' for x in range(2, 135)]) # This extends the url_pages list to have the list of the pages from 2 to 111.

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    for x in url_pages:
        try: 
            response = requests.get(x, headers=headers)

            soup = BeautifulSoup(response.content, 'html.parser')

            title_elements = soup.find_all('span', class_='relative top-[2px] hidden md:inline')
            
            for title in title_elements:
                title_text = title.get_text(strip=True)
                titles.append(title_text)

            location_elements = soup.find_all('p', class_='ml-1 truncate text-sm font-normal capitalize text-grey-650')

            for location in location_elements:
                location_text = location.get_text(strip=True)
                locations.append(location_text)

            # Extract only unique price values from the current page
            price_elements = soup.find_all('a', class_='no-underline')
            all_text = " ".join([element.get_text(strip=True) for element in price_elements])

            # Find price occurrences and remove duplicates
            found_prices = list(set(re.findall(r'KSh\s[\d,]+', all_text)))  
            prices.extend([price.replace("KSh", "").strip() for price in found_prices])

            time.sleep(response.elapsed.total_seconds()) # Make another request after the time spent to make the last request. 
        except Exception as e:
            print(f'Error: {str(e)}')

    properties.append({
        'titles': titles,
        "locations": locations,
        "prices": prices
    })

    print(f'{len(titles)} titles scrapped successfully!')
    print(f'{len(locations)} titles scrapped successfully!')
    print(f'{len(prices)} titles scrapped successfully!')

    with open('new_data.json', 'w') as f:
        json.dump(properties, f, indent=4)


if __name__ == '__main__':
    scrape()






