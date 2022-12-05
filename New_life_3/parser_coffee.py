from bs4 import BeautifulSoup
import requests

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
}

coffee_urls = []
coffee_title = []


def coffee_city():
    url = f'https://restaurantguru.ru/coffeehouse-Gomel-t5'

    response = requests.get(url=url, headers=headers)

    pages_info = BeautifulSoup(response.text, 'html.parser')

    coffee_shops = pages_info.find_all('div', class_='wrapper_info')
    for coffee in coffee_shops:
        urls = coffee.find('div', class_='title').find('a').get('href')
        title = coffee.find('div', class_='title').find('a').text

        coffee_urls.append(urls)
        coffee_title.append(title)
    return coffee_urls, coffee_title


coffee_city()
