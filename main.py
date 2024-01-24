import pytz
from telethon.sync import TelegramClient
from telethon import functions, types
import asyncio
from dotenv import load_dotenv
import os
import datetime

from services import writing_json, reading_json, get_key_phrase

load_dotenv('.env')  # загружаем данные из виртуального окружения

api_id = os.getenv('TELEGRAM_API_ID')  # получаем api_id, полученный у Telegram
api_hash = os.getenv('TELEGRAM_API_HASH')  # получаем api_hash, полученный у Telegram
key_word = 'gurienomika'

# список ключевых слов
key_words = ['биржа', 'фриланс', 'заказ', 'сайт', 'реклама', 'удаленно', 'сделать']

file_data = os.path.abspath('./channels.json')  # файл для хранения списка вакансий

desired_timezone = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс
date_time_now = datetime.datetime.now()  # получаем текущие дату и время

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

    # Получаем диалоги пользователя
    # dialogs = await client.get_dialogs(limit=2)
    # print(dialogs)

    # Фильтруем диалоги по ключевому слову
    # result = [dialog.entity for dialog in dialogs if ключевое_слово.lower() in dialog.name.lower()]

    # print(result.stringify())
    chat_list = result.chats  # получаем список каналов из ответа Telegram
    print(f"Найдено каналов: {len(chat_list)}")

    # получаем список каналов из файла хранения
    # если файла еще не существует, будет создан пустой список
    channels_list = reading_json(file_data)

    # перебираем список спарсенных каналов
    for chat in chat_list:
        channel_dict = {}  # создаем словарь, в который будем складывать данные о канале
        if chat.username:
            chat_link = f"https://t.me/{chat.username}"
        else:
            chat_link = None
        print(f"ID канала: {chat.id}, Название: {chat.title}, Ссылка на канал: {chat_link}")
        channel_dict['id'] = chat.id
        channel_dict['title'] = chat.title
        channel_dict['link'] = chat_link

        # проверяем последнее сообщение в канале
        async for message in client.iter_messages(chat.title, limit=1):
            # print(message.date)

            # преобразуем даты с учетом часового пояса
            time_now = date_time_now.astimezone(desired_timezone)  # текущее время с учетом часового пояса
            time_massage = message.date.astimezone(desired_timezone)  # время сообщения с учетом часового пояса

            # проверяем давность сообщения (если сообщение опубликовано не позднее 7 дней)
            if (time_now.date() - time_massage.date()).days <= 7:
                if channel_dict not in channels_list:  # если канала нет в списке, добавляем в список
                    channels_list.append(channel_dict)

    writing_json(file_data, channels_list)  # сохраняем список каналов в файл в формате json

    await client.disconnect()

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_channels_by_keyword())
