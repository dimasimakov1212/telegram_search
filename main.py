from telethon.sync import TelegramClient
from telethon import functions, types
import asyncio
import time

from channels import get_channels_by_keyword, file_data_json
from services import reading_json


def get_channels():
    """ Функция поиска каналов """

    channels_list = reading_json(file_data_json)  # получаем список каналов из файла хранения
    len_channels_list_start = len(channels_list)  # определяем начальное количество каналов

    loop = asyncio.get_event_loop()  # получаем текущий цикл событий

    # запускаем цикл поиска каналов, количество итераций можно изменить
    for i in range(2):
        loop.run_until_complete(get_channels_by_keyword())  # запускаем цикл событий
        print('----- ожидайте -----')
        time.sleep(20)

    channels_list = reading_json(file_data_json)  # получаем список каналов из файла хранения
    len_channels_list_end = len(channels_list)  # определяем конечное количество каналов

    len_difference = len_channels_list_end - len_channels_list_start  # определяем разницу в количестве каналов

    print(f"Добавлено {len_difference} новых каналов")
    print(f"Всего каналов в файле: {len_channels_list_end}")


if __name__ == '__main__':

    get_channels()  # запуск поиска каналов

# Получаем диалоги пользователя
# dialogs = await client.get_dialogs(limit=2)
# print(dialogs)

# Фильтруем диалоги по ключевому слову
# result = [dialog.entity for dialog in dialogs if ключевое_слово.lower() in dialog.name.lower()]
