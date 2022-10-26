import requests
import logging
import os
from dotenv import load_dotenv
from os.path import splitext
from urllib.parse import unquote, urlsplit


def get_vk_response(access_vk_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': access_vk_token,
        'v': 5.131,
        'group_id': group_id,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


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
    load_dotenv()
    access_vk_token = os.getenv('ACCESS_VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    logging.basicConfig(level=logging.DEBUG)

    # logging.info('Получение ответа от xkcd...')
    #
    # xkcd_response = get_xkcd_answer()
    # # download_comic(xkcd_response)
    #
    # logging.info('Получение комментария к картинке xkcd...')
    # xkcd_comment = xkcd_response['alt']
    # print(xkcd_comment)

    vk_response = get_vk_response(access_vk_token, group_id)
    print(vk_response)

