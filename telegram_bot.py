import os

import telebot
from telebot import types
from dotenv import load_dotenv

from main import get_channels

load_dotenv('.env')  # загружаем данные из виртуального окружения

bot_token = os.getenv('TELEGRAM_ACCESS_TOKEN')  # получаем токен бота

bot = telebot.TeleBot(bot_token)  # создаем бота


@bot.message_handler(commands=['start'])
def start_bot(massage):
    """ Функция запуска меню бота """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем клавиатуру бота
    button_1 = types.KeyboardButton('Старт')  # создаем кнопку
    button_2 = types.KeyboardButton('Инфо')  # создаем кнопку
    markup.add(button_1, button_2)  # добавляем кнопки в клавиатуру бота

    # отправляем в бот приветствие и запускам клавиатуру
    bot.send_message(massage.chat.id, 'Привет, {0.first_name}!'.format(massage.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_massage(massage):
    """ Функция работы меню бота """

    # если в меню бота нажать кнопку "Инфо"
    if massage.text == 'Инфо':
        # отправляется сообщение с ником пользователя
        bot.send_message(massage.chat.id, 'Твой ник: @{0.username}'.format(massage.from_user))

    # если в меню бота нажать кнопку "Старт"
    elif massage.text == 'Старт':
        bot.send_message(massage.chat.id, 'Ожидайте, идет поиск...')

        # запускается поиск Telegram каналов
        new_channels = get_channels()

        bot.send_message(massage.chat.id, f'Найдено {new_channels} новых каналов')
        # bot.send_message(massage.chat.id, 'Привет, {0.first_name}!'.format(massage.from_user))


bot.polling(non_stop=True)  # команда, чтобы бот не отключался
