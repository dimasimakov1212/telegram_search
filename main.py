from pathlib import Path

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types
import asyncio
from dotenv import load_dotenv
import os

load_dotenv('.env')

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
key_word = 'получить кредит'

# Создаем клиент Telegram
client = TelegramClient('session_name', api_id, api_hash)


async def get_channels_by_keyword():
    await client.start()

    # Ищем каналы по ключевому слову
    result = await client(functions.contacts.SearchRequest(
        q=key_word,
        limit=15
    ))  # Можете увеличить или уменьшить лимит

    # print(result.stringify())
    chat_list = result.chats
    print(len(chat_list))

    for chat in chat_list:
        print(f"ID канала: {chat.id}, Название: {chat.title}")

    # Выводим информацию о найденных каналах
    # for entity in result:
    #
    #     if hasattr(entity, 'channel'):
    #         print(f"ID канала: {entity.channel.id}, Название: {entity.channel.title}")

    await client.disconnect()

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_channels_by_keyword())
