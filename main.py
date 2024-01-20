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
key_word = 'котики и фотики'

# Создаем клиент Telegram
client = TelegramClient('session_name', api_id, api_hash)


async def get_channels_by_keyword():
    await client.start()

    # Ищем каналы по ключевому слову
    result = await client(functions.contacts.SearchRequest(
        q=key_word,
        limit=15
    ))  # Можете увеличить или уменьшить лимит

    # Получаем диалоги пользователя
    # dialogs = await client.get_dialogs(limit=2)
    # print(dialogs)

    # Фильтруем диалоги по ключевому слову
    # result = [dialog.entity for dialog in dialogs if ключевое_слово.lower() in dialog.name.lower()]

    # print(result.stringify())
    chat_list = result.chats
    print(len(chat_list))

    for chat in chat_list:
        chat_link = f"https://t.me/{chat.username}"
        print(f"ID канала: {chat.id}, Название: {chat.title}, Ссылка на канал: {chat_link}")

    # Выводим информацию о найденных каналах
    # for entity in result:
    #
    #     if hasattr(entity, 'channel'):
    #         print(f"ID канала: {entity.channel.id}, Название: {entity.channel.title}")

    await client.disconnect()

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_channels_by_keyword())
