from telethon.sync import TelegramClient
from telethon import functions
from dotenv import load_dotenv
import os

from services import writing_json, reading_json, get_key_phrase, get_days_difference

load_dotenv('.env')  # загружаем данные из виртуального окружения

api_id = os.getenv('TELEGRAM_API_ID')  # получаем api_id, полученный у Telegram
api_hash = os.getenv('TELEGRAM_API_HASH')  # получаем api_hash, полученный у Telegram
key_word = 'gurienomika'

# список ключевых слов из которых будет составлена ключевая фраза
key_words = ['биржа', 'фриланс', 'заказ', 'сайт', 'реклама', 'удаленно', 'сделать']

# список слов, при наличии которых в названии канала, канал не будет добавлен
stop_words = ['oriflame', 'спецтехники', 'отзывов', 'клипы', 'wildberries', 'исламский']

file_data_json = os.path.abspath('./channels.json')  # файл для хранения списка вакансий

# Создаем клиент Telegram
client = TelegramClient('session_name', api_id, api_hash)


async def get_channels_by_keyword():
    """ Функция поиска каналов по ключевым словам """

    await client.start()  # запускаем сессию клиента Telegram

    key_phrase = get_key_phrase(key_words)  # получаем ключевую фразу
    print(f"Ключевая фраза: {key_phrase}")

    # Ищем каналы по ключевой фразе
    result = await client(functions.contacts.SearchRequest(
        q=key_phrase,
        limit=10  # Можно увеличить или уменьшить лимит, однако Telegram не выдает больше 10 вариантов
    ))

    # print(result.stringify())
    chat_list = result.chats  # получаем список каналов из ответа Telegram
    print(f"Найдено каналов: {len(chat_list)}")

    # получаем список каналов из файла хранения
    # если файла еще не существует, будет создан пустой список
    channels_list = reading_json(file_data_json)

    # перебираем список спарсенных каналов
    for chat in chat_list:

        channel_dict = {}  # создаем словарь, в который будем складывать данные о канале
        if chat.username:
            chat_link = f"https://t.me/{chat.username}"  # формируем ссылку на канал, если она доступна
        else:
            chat_link = None
        print(f"ID канала: {chat.id}, Название: {chat.title}, Ссылка на канал: {chat_link}")
        channel_dict['id'] = chat.id  # id канала
        channel_dict['title'] = chat.title  # название канала
        channel_dict['link'] = chat_link  # ссылка на канал

        for word in stop_words:  # проверяем наличие в названии канала стоп-слов

            if word.lower() not in chat.title.lower().split():  # если стоп-слова нет в названии канала

                # проверяем последнее сообщение в канале
                async for message in client.iter_messages(chat.title, limit=1):
                    # print(message.date)

                    # определяем давность последнего сообщения в днях от текущей даты
                    days_difference = get_days_difference(message.date)

                    # проверяем давность сообщения (чтобы сообщение было опубликовано не позднее 7 дней)
                    if days_difference <= 7:

                        if channel_dict not in channels_list:  # если канала нет в списке, добавляем в список
                            channels_list.append(channel_dict)

    writing_json(file_data_json, channels_list)  # сохраняем список каналов в файл в формате json

    await client.disconnect()
