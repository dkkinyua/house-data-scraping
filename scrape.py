import re
import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.buyrentkenya.com/houses-for-sale'

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
try: 
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find_all('span', class_='relative top-[2px] hidden md:inline')
    title_text = [i.text.strip() if i else "No Title" for i in title]

    location = soup.find_all('p', class_='ml-1 truncate text-sm font-normal capitalize text-grey-650')
    location_text = [x.text.strip() if x else 'No Location' for x in location]
    # print(location_text)

    price = soup.find_all('a', class_='no-underline')
    price_text = [i.text.strip() for i in price if re.match(r'KSh \d{1,3}(?:,\d{3})*(?:\.\d+)?|Price not communicated', i.text.strip())]
    # print(price_text)
    
except Exception as e:
    print(f'Error: {str(e)}')
