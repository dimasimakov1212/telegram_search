from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types
import asyncio
from dotenv import load_dotenv
import os

from services import writing_json, reading_json

load_dotenv('.env')

api_id = os.getenv('TELEGRAM_API_ID')  # получаем api_id, полученный у Telegram
api_hash = os.getenv('TELEGRAM_API_HASH')  # получаем api_hash, полученный у Telegram
key_word = 'котики и фотики'

# Создаем клиент Telegram
client = TelegramClient('session_name', api_id, api_hash)


async def get_channels_by_keyword():
    """ Функция поиска каналов по ключевым словам """

    await client.start()  # запускаем сессию клиента Telegram

    # Ищем каналы по ключевому слову
    result = await client(functions.contacts.SearchRequest(
        q=key_word,
        limit=10
    ))  # Можно увеличить или уменьшить лимит, однако Telegram не выдает больше 10 вариантов

    # Получаем диалоги пользователя
    # dialogs = await client.get_dialogs(limit=2)
    # print(dialogs)

    # Фильтруем диалоги по ключевому слову
    # result = [dialog.entity for dialog in dialogs if ключевое_слово.lower() in dialog.name.lower()]

    # print(result.stringify())
    chat_list = result.chats  # получаем список каналов из ответа Telegram
    print(len(chat_list))

    # получаем список каналов из файла хранения
    # если файла еще не существует, будет создан пустой список
    channels_list = reading_json

    # перебираем список каналов
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

        channels_list.append(channel_dict)

    writing_json(channels_list)
    # print(channels_list)

    # Выводим информацию о найденных каналах
    # for entity in result:
    #
    #     if hasattr(entity, 'channel'):
    #         print(f"ID канала: {entity.channel.id}, Название: {entity.channel.title}")

    await client.disconnect()

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_channels_by_keyword())
