from bs4 import BeautifulSoup
import requests

film_urls = []
title_film = []
time_film = []
cash_film = []


def cinema():
    url = 'https://afisha.relax.by/place/id/3294/'

    response = requests.get(url=url)
    print(response)

    pages_info = BeautifulSoup(response.text, 'html.parser')

    films = pages_info.find_all('div', class_='schedule__item table_by_place rubric_place')

    for film in films:
        urls = film.find('div', class_='schedule__event').find('div', class_='schedule__place_wrap').find('a').get('href')
        title = film.find('div', class_='schedule__event').find('div', class_='schedule__place_wrap').find('a').text
        time = film.find('div', class_='schedule__seance-wrap').find('a').text
        cash = film.find('div', class_='schedule__seance-wrap').find('span').text

        film_urls.append(urls.strip())
        title_film.append(title.strip())
        time_film.append(time.strip())
        cash_film.append(cash.strip())

        return film_urls, title_film, time_film, cash_film


cinema()