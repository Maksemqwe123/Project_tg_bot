from bs4 import BeautifulSoup
import requests

coffee_urls = []
coffee_title = []
coffee_address = []


def coffee_minsk():
    url = 'https://zoon.by/minsk/restaurants/type/kofejni/'

    response = requests.get(url=url)

    pages_info = BeautifulSoup(response.text, 'html.parser')

    coffee_shops = pages_info.find_all('div', class_='minicard-item__info')

    for coffee in coffee_shops:
        urls = coffee.find('h2', class_='minicard-item__title').find('a').get('href')
        title = coffee.find('h2', class_='minicard-item__title').find('a').text
        address = coffee.find('address', class_='minicard-item__address').find('span', class_='address').text

        coffee_urls.append(urls)
        coffee_title.append(title)
        coffee_address.append(address)

        return coffee_urls, coffee_title, coffee_address


coffee_minsk()