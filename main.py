import telebot, requests, json
from telebot import types
token = '6134943560:AAG79Dza7t287LRS9iuND4GxRt03Mc-N-GU'
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте!')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Калькулятор")
    item2 = types.KeyboardButton("Погода")
    item3 = types.KeyboardButton("Переводчик")
    item4 = types.KeyboardButton("Мем дня")
    item5 = types.KeyboardButton("Выход")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(message.chat.id,'Выберите что вам надо:',reply_markup=markup)
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Калькулятор":
        bot.send_message(message.chat.id, '1')

    elif message.text=="Погода":
        bot.send_message(message.chat.id, '2')

    elif message.text=="Переводчик":
        bot.send_message(message.chat.id, '3')

    elif message.text=="Мем дня":
        bot.send_message(message.chat.id, '4')

    elif message.text=="Выход":
        bot.send_message(message.chat.id, 'До свидания, спасибо за использование бота')


bot.polling(none_stop=True)
