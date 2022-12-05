from bs4 import BeautifulSoup
import requests

pizza_urls = []
pizza_title = []
pizza_address = []
pizza_time_work = []


def restaurant():
    url = 'https://zabava.by/restaurant/pitstseriya'

    response = requests.get(url=url)

    pages_info = BeautifulSoup(response.text, 'html.parser')

    restaurant_pizza = pages_info.find_all('div', class_='info')

    for pizza in restaurant_pizza:
        urls = pizza.find('div', class_='leftBlock').find('a').get('href')
        title = pizza.find('div', class_='name-rating').find('a').text
        address = pizza.find('div', class_='rightBlock').find('div', class_='address').text
        time_work = pizza.find('div', class_='rightBlock').find('div', class_='time').text

        pizza_urls.append(urls)
        pizza_title.append(title)
        pizza_address.append(address.strip())
        pizza_time_work.append(time_work.strip())

        return pizza_urls, pizza_title, pizza_address, pizza_time_work


restaurant()