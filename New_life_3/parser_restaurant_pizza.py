from bs4 import BeautifulSoup
import requests

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
}

pizza_urls = []
pizza_title = []
pizza_address = []
pizza_time_work = []


def restaurant():
    url = f'https://gomel.jsprav.ru/pitstserii/'

    response = requests.get(url=url, headers=headers)

    pages_info = BeautifulSoup(response.text, 'html.parser')

    restaurant_pizza = pages_info.find_all('div', class_='company-info-c')

    for pizza in restaurant_pizza:
        urls = pizza.find('h3', class_='company-info-name').find('a').get('href')
        title = pizza.find('h3', class_='company-info-name').find('span').text
        address = pizza.find('div', class_='company-info-address company-info-data company-info-data-only').find('address', class_='company-info-address-full company-info-text').text
        time_work = pizza.find('div', class_='company-info-time company-info-data company-info-data-only').find('span', class_='company-info-time-full company-info-text').text

        pizza_urls.append(urls)
        pizza_title.append(title)
        pizza_address.append(address.strip())
        pizza_time_work.append(time_work.strip())

    return pizza_urls, pizza_title, pizza_address, pizza_time_work


restaurant()