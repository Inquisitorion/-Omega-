import requests
import telebot
import time
import random
import math
from telebot import types
from googletrans import Translator
from bs4 import BeautifulSoup

BOT_TOKEN = '6055944515:AAHcWV5qpCTH1ouoFvHslXLMx6jK7ZeAGqs'
bot = telebot.TeleBot(BOT_TOKEN)

TIMEOUT_CONNECTION = 5
START_MESSAGE = "Привет, я omega."
bd = [{'user_id': '0', 'state': 'default'}]

urltl = 'https://api.telegram.org/bot'


def make_bd(message):
    already_have = False
    for user in bd:
        if user['user_id'] == message.chat.id:
            already_have = True

    if not already_have:
        bd.append({'user_id': message.chat.id, 'state': 'default'})
    print(bd)


@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🈳Переводчик')
    item2 = types.KeyboardButton('➗Калькулятор')
    item3 = types.KeyboardButton('🔆Погода')
    item4 = types.KeyboardButton('😈Мемы')
    item5 = types.KeyboardButton('👁‍🗨Информация')
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, 'Сделай выбор, user!', reply_markup=markup)
    make_bd(message)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    item_back = types.KeyboardButton('Назад')
    item1 = types.KeyboardButton('🈳Переводчик')
    item2 = types.KeyboardButton('➗Калькулятор')
    item3 = types.KeyboardButton('🔆Погода')
    item4 = types.KeyboardButton('😈Мемы')
    item5 = types.KeyboardButton('👁‍🗨Информация')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    make_bd(message)

    for i in bd:
        if i['user_id'] == message.chat.id:
            user = i

    if message.chat.type == 'private':
        if message.text == '🈳Переводчик':
            markup.add(item_back, item5)
            bot.send_message(message.chat.id, 'Введите текст для перевода', reply_markup=markup)
            user['state'] = 'translate'

        elif message.text == '➗Калькулятор':
            markup.add(item_back, item5)
            bot.send_message(message.chat.id, 'Введите выражение для посчитать', reply_markup=markup)
            user['state'] = 'calculate'

        elif message.text == '🔆Погода':
            markup.add(item_back, item5)
            bot.send_message(message.chat.id, 'Введите город, чтобы узнать погоду', reply_markup=markup)
            user['state'] = 'weather'

        elif message.text == '😈Мемы':
            markup.add(item_back, item5)
            bot.send_message(message.chat.id, 'Пришлю вам прикол ГЫ-ГЫ-ГЫ!', reply_markup=markup)
            user['state'] = 'memes'
            memes(message)


        elif message.text == '👁‍🗨Информация':
            if user['state'] == 'default':
                bot.send_message(message.chat.id, 'СПБГУТ ИКПИ-12 Соколов Егор, Проскуряк Влад')
            elif user['state'] == 'calculate':
                bot.send_message(message.chat.id, 'Вам доступны базовые арифметические операци')
            elif user['state'] == 'translate':
                bot.send_message(message.chat.id, 'В боте доступно два языка: RU, EN')
            elif user['state'] == 'weather':
                bot.send_message(message.chat.id, 'Бот знает погоду во всех городах мира')
            elif user['state'] == 'memes':
                bot.send_message(message.chat.id, 'Бот умеет скидывать рандомный мем')

        elif message.text == 'Назад':
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id, '0-Назад', reply_markup=markup)
            user['state'] = 'default'

        else:
            if user['state'] == 'calculate':
                calculator(message)
            elif user['state'] == 'translate':

                translator(message)
            elif user['state'] == 'weather':
                weather(message)
            elif user['state'] == 'memes':
                memes(message)


def translator(message):
    if message.text:
        translator = Translator(service_urls=['translate.google.com'])
        translation = translator.translate(message.text,
                                           dest='ru' if translator.detect(message.text).lang == 'en' else 'en')
        translated_text = translation.text
        bot.send_message(message.chat.id, f'Переведенный текст:\n\n{translated_text}')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите текст для перевода.')

def memes(message):
        img_url = f'https://t.me/memes_prog/%7Brandom.randint(1, 1000)'
        request_url = f'{urltl}{BOT_TOKEN}/sendPhoto?chat_id={message.chat.id}&photo={img_url}'
        requests.get(request_url)


# погода
def weather(message):
    weather_api_key = '54e6869ab9c8a14b92e5ada3bbd43ee6'
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ru&units=metric&appid={weather_api_key}")
        data = response.json()

        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        bot.send_message(message.chat.id,
                         f"Погода в городе: {city}\nТемпература: {cur_temp}°C\nВлажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\nВетер: {wind} м/с \nХорошего дня!")
    except:
        bot.send_message(message.chat.id, 'Проверьте название города!')


def calculator(message):
    msg = None
    user_message = message.text.lower()
    user_message = user_message.lstrip()
    user_message = user_message.rstrip()
    answer = str(eval(user_message.replace(' ', '')))
    msg = bot.send_message(message.chat.id, user_message.replace(' ', '') + ' = ' + answer)


# Вход в программу
if __name__ == '__main__':

    bot.polling()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print('Ошибка подключения. Я устал!' % TIMEOUT_CONNECTION)
            time.sleep(TIMEOUT_CONNECTION)

