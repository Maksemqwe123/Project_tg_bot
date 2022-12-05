from bs4 import BeautifulSoup
import requests

list_pizza = []


def deals():
    url = f'https://ym1.by/akczii/'

    response = requests.get(url=url)

    pages_info = BeautifulSoup(response.text, 'html.parser')

    pizza = pages_info.find('article', class_='akcii-i post-1011 akczii type-akczii status-publish has-post-thumbnail hentry').find('a').get('href')
    list_pizza.append(pizza)

    return list_pizza


parser_pizza = deals()
