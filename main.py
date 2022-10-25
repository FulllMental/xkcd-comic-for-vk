import requests
import logging
from os.path import splitext
from urllib.parse import unquote, urlsplit


def get_xkcd_answer():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()


def get_picture_extension(image_url):
    
    logging.info('Выделение расширения файла...')
    link_split = urlsplit(image_url)
    file_name = unquote(link_split[2])
    file_extension = splitext(file_name)
    return file_extension[1]


def download_comic(xkcd_response):
    image_url = xkcd_response['img']
    extension = get_picture_extension(image_url)
    filename = f'comic{extension}'

    logging.info('Скачивание картинки...')
    response = requests.get(image_url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Получение ответа от xkcd...')

    xkcd_response = get_xkcd_answer()
    download_comic(xkcd_response)
