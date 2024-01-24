import json
import os

file_data = os.path.abspath('channels.json')  # файл для хранения списка вакансий


def writing_json(channels_list):
    """ Записывает данные в формате json """

    with open(file_data, 'w', encoding='utf-8') as file:
        json.dump(channels_list, file, sort_keys=False, indent=4, ensure_ascii=False)


def reading_json():
    """ Считывает данные из формата json """

    try:
        with open(file_data, 'r', encoding='utf-8') as file:
            channels = json.load(file)
        return channels
    except FileNotFoundError:
        print('Такого файла не существует, будет создан новый файл')
        channels = []
        return channels
