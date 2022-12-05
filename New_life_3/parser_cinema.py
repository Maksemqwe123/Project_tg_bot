from bs4 import BeautifulSoup
import requests

film_urls = []
title_film = []
time_film = []


def cinema():
    url = f'https://afisha.me/place/oktyabr-gomel/'

    response = requests.get(url=url)

    pages_info = BeautifulSoup(response.text, 'html.parser')

    films = pages_info.find_all('div', class_='event-item-i js-film-list__li')

    for film in films:
        urls = film.find('div', class_='item-header').find('div', class_='item-header-i').find('a').get('href')
        title = film.find('div', class_='item-header').find('div', class_='item-header-i').find('a').text
        time = film.find('div', class_='event-session js-session-list-wrapper').find('ul', class_='b-shedule__list js-shedule-list').find('li', class_='shedule__li').text

        film_urls.append(urls.strip())
        title_film.append(title.strip())
        time_film.append(time.strip())

    return film_urls, title_film, time_film


cinema()