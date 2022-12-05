from aiogram.dispatcher.filters import Text, Command
from weather_tg_bot import dp, bot, types
from New_life_3.weatear import ru
from config import OPEN_WEATHER_TOKEN, ADMIN_ID
from buttons import user_kb, house_or_street, help_assistant_house, help_assistant_street, cities, menu
from parser_pizza import list_pizza
from parser_kinogo import kinogo_urls, kinogo_decription
from parser_litres import list_urls, litres_description
from cook_parser import cook_urls, cook_description
from parser_cinema import film_urls, title_film, time_film
from parser_restaurant_pizza import pizza_urls, pizza_title, pizza_address, pizza_time_work
from parser_coffee import coffee_urls, coffee_title
from sqlite import Database
import requests
import random
import datetime
import os

db = Database('database.db')

count_of_attempts = 1
number = random.randint(1, 12)
print(number)


@dp.message_handler(commands='start')
async def start_Message(message: types.Message):
    if message.chat.type == 'private':
        if not db.create_profile(message.from_user.id):
            db.edit_profile(message.from_user.id)
        await message.answer('Привет, я бот который подскажет как провести день, в связи с погодой',
                             reply_markup=user_kb)
        await message.answer('В каком городе ты хочешь узнать погоду?🌤')


@dp.message_handler(commands='sendall')
async def send_all(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == ADMIN_ID:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)

                except:
                    db.set_active(row[0], 0)

            await bot.send_message(message.from_user.id, "Успешная рассылка")


@dp.message_handler(Text(equals=cities, ignore_case=True))
async def today(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={OPEN_WEATHER_TOKEN}&units=metric&lang={ru}"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        await message.answer(f'В городе: {city} \nТемпература воздуха: {cur_weather} C \nОжидается: {weather_description}\n'
                             f'Скорость ветра: {wind} м/c', reply_markup=house_or_street)

        if cur_weather < 5 and cur_weather > -4:
            await message.answer('cегодня на улице немного холодно, возможно слякоть и гололёд,'
                                 'можно остаться дома или пойти на улицу')

        elif cur_weather < -4 and cur_weather > -8:
            await message.answer('сейчас на улице холодно, оденься потеплее, желательно ещё поесть перед выходом')

        elif cur_weather < -9 and cur_weather > -16:
            await message.answer('сейчас на улице довольно холодно, посоветую тебе остаться дома,'
                                 ' но если тебе не страшен холод, могу посоветовать куда можно сходить  ')

        elif cur_weather < -16:
            await message.answer('cейчас на улице очень холодно, останься лучше дома')


    except:
        await message.reply("Проверьте название города")


@dp.message_handler(Text(equals='Что можно поделать дома ?🏠', ignore_case=True))
async def leisure(message: types.Message):
    await message.answer('можно посмотреть/почитать фильм/книгу, но перед этим, я бы посоветовал заварить чая/кофе.\n'
                         'могу подсказать как легко и просто приготовить вкусный десерт,'
                         'так же проходит акция при заказе пиццы', reply_markup=help_assistant_house)


@dp.message_handler(Text(equals='Как можно провести время на улице ?🚶‍♂🚶‍♀', ignore_case=True))
async def street(message: types.Message):
    await message.answer('Можно сходить в кино/театр, можно весело провести время катаясь на коньках.'
                         'В холодную погоду не помешает выпить кофе/чая. Также можно пройтись по прекрасному парку,'
                         'а в конце вечера можно сходить покушать пиццы', reply_markup=help_assistant_street)


@dp.message_handler(Text(equals='Узнать погоду в городе🌤', ignore_case=True))
async def back(message: types.Message):
    await message.answer('Погода на сегодня ожидается...', reply_markup=user_kb)


@dp.message_handler(Text(equals='Сыграть в игру🔮', ignore_case=True))
async def game(message: types.Message):
    global count_of_attempts, number

    if count_of_attempts == 1:
        await message.answer(f'Отгадай число \nя загадал число от 1 до 20, попробуй его угадать😉', reply_markup=menu)
    else:
        await message.answer(f'Введите число🧐')


@dp.message_handler(Text(equals='Выйти в главное меню📋', ignore_case=True))
async def back(message: types.Message):
    await message.answer('секунду⏱', reply_markup=house_or_street)


@dp.message_handler(Text(equals='Как можно провести время на улице ?🚶‍♂🚶‍♀', ignore_case=True))
async def back_street(message: types.Message):
    await message.answer('Сейчас подскажу', reply_markup=help_assistant_street)


@dp.message_handler(Text(equals='Что можно поделать дома ?🏠', ignore_case=True))
async def back_street(message: types.Message):
    await message.answer('Сейчас подскажу', reply_markup=help_assistant_house)


@dp.message_handler(Text(equals='Что за акция на пиццу?🍕', ignore_case=True))
async def pizza(message: types.Message):
    await message.answer(f'{list_pizza}')


@dp.message_handler(Text(equals='Какой фильм можно посмотреть?🎬', ignore_case=True))
async def kinogo(message: types.Message):
    await message.answer(f'Название: {kinogo_decription[1]} \nCcылка: {kinogo_urls[1]}\n')
    await message.answer(f'Название: {kinogo_decription[2]} \nCcылка: {kinogo_urls[2]}\n')
    await message.answer(f'Название: {kinogo_decription[3]} \nCcылка: {kinogo_urls[3]}\n')
    await message.answer(f'Название: {kinogo_decription[4]} \nCcылка: {kinogo_urls[4]}\n')


@dp.message_handler(Text(equals='Какую книгу можно почитать?📚', ignore_case=True))
async def book(message: types.Message):
    await message.answer(f'Название:{litres_description[1]} \nCcылка: {list_urls[1]}\n')
    await message.answer(f'Название:{litres_description[2]} \nCcылка: {list_urls[2]}\n')
    await message.answer(f'Название:{litres_description[3]} \nCcылка: {list_urls[3]}\n')
    await message.answer(f'Название:{litres_description[4]} \nCcылка: {list_urls[4]}\n')


@dp.message_handler(Text(equals='Какой десерт можно легко приготовить?🧁', ignore_case=True))
async def cook(message: types.Message):
    await message.answer(f'Название: {cook_description[1]} \nCcылка: {cook_urls[1]}\n')
    await message.answer(f'Название: {cook_description[2]} \nCcылка: {cook_urls[2]}\n')
    await message.answer(f'Название: {cook_description[3]} \nCcылка: {cook_urls[3]}\n')
    await message.answer(f'Название: {cook_description[4]} \nCcылка: {cook_urls[4]}\n')


@dp.message_handler(Text(equals='На какой фильм в кинотеатр можно сходить ?🎬', ignore_case=True))
async def cinema(message: types.Message):
    await message.answer(f'Название: {title_film[1]} \nCcылка: {film_urls[1]}\nВремя и стоимость:{time_film[1]}')
    await message.answer(f'Название: {title_film[2]} \nCcылка: {film_urls[2]}\nВремя и стоимость:{time_film[2]}')
    await message.answer(f'Название: {title_film[3]} \nCcылка: {film_urls[3]}\nВремя и стоимость:{time_film[3]}')
    await message.answer(f'Название: {title_film[4]} \nCcылка: {film_urls[4]}\nВремя и стоимость:{time_film[4]}')


@dp.message_handler(Text(equals='Куда можно сходить поесть ?🍽', ignore_case=True))
async def cinema(message: types.Message):
    await message.answer(f'Название: {pizza_title[0]} \nCcылка: {pizza_urls[0]} \nНаходится: {pizza_address[0]} '
                         f'\nВремя работы: {pizza_time_work[0]}')
    await message.answer(f'Название: {pizza_title[1]} \nCcылка: {pizza_urls[1]} \nНаходится: {pizza_address[1]} '
                         f'\nВремя работы: {pizza_time_work[1]}')
    await message.answer(f'Название: {pizza_title[2]} \nCcылка: {pizza_urls[2]} \nНаходится: {pizza_address[2]} '
                         f'\nВремя работы: {pizza_time_work[2]}')


@dp.message_handler(Text(equals='Где и какой кофе можно выпить?☕️', ignore_case=True))
async def coffee(message: types.Message):
    await message.answer(f'Название: {coffee_title[0]} \nCcылка: {coffee_urls[0]}')
    await message.answer(f'Название: {coffee_title[1]} \nCcылка: {coffee_urls[1]}')
    await message.answer(f'Название: {coffee_title[2]} \nCcылка: {coffee_urls[2]}')
    await message.answer(f'Название: {coffee_title[3]} \nCcылка: {coffee_urls[3]}')

# @dp.message_handler(Text(equals='Какое представление можно посмотреть?', ignore_case=True))
# async def theatre(message: types.Message):
#     await message.answer(f'Название: {theatre_title[0]} \n{theatre_urls[0]} \nАдрес: {theatre_address[0]}'
#                          f'\nНачало:{theatre_time[0]} \nCтоимость: {theatre_cash[0]}')
#     await message.answer(f'Название: {theatre_title[1]} \n{theatre_urls[1]} \nАдрес: {theatre_address[1]}'
#                          f'\nНачало: {theatre_time[1]} \nCтоимость: {theatre_cash[1]}')
#     await message.answer(f'Название: {theatre_title[2]} \n{theatre_urls[2]} \nАдрес: {theatre_address[2]}'
#                          f'\nНачало: {theatre_time[2]} \nCтоимость: {theatre_cash[2]}')
#     await message.answer(f'Название: {theatre_title[3]} \n{theatre_urls[3]} \nАдрес: {theatre_address[3]}'
#                          f'\nНачало: {theatre_time[3]} \nCтоимость: {theatre_cash[3]}')


@dp.message_handler()
async def info(message: types.Message):
    global number, count_of_attempts

    try:
        if int(message.text) == number:
            await message.answer(f'Вы угадали!🎉\nКоличество попыток: {count_of_attempts}')

        elif int(message.text) < number:
            await message.answer(f'Введенное число меньше загаданного')
            count_of_attempts += 1
            await game(message)

        else:
            await message.answer(f'Введенное число больше загаданного')
            count_of_attempts += 1
            await game(message)
    except ValueError:
        await message.answer(f'Ошибка❗\nДанные должны иметь числовой тип')
        await game(message)