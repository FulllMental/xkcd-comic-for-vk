import requests
import logging
import os
from dotenv import load_dotenv
from os.path import splitext
from urllib.parse import unquote, urlsplit


def upload_vk_picture(access_vk_token, group_id, filename):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': access_vk_token,
        'v': 5.131,
        'group_id': group_id,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    upload_url = response.json()['response']['upload_url']
    with open(filename, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        return response.json()


def save_vk_picture(access_vk_token, group_id, upload_response):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    photo = upload_response['photo']
    server = upload_response['server']
    vk_hash = upload_response['hash']
    payload = {
        'access_token': access_vk_token,
        'v': 5.131,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': vk_hash,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    print(response.json())

def get_xkcd_answer():

    logging.info('Получение ответа от xkcd...')
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()


def get_picture_extension(image_url):

    logging.info('Выделение расширения файла...')
    link_split = urlsplit(image_url)
    file_name = unquote(link_split[2])
    file_extension = splitext(file_name)
    return file_extension[1]


def download_comic(image_url, filename):

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

    xkcd_response = get_xkcd_answer()
    image_url = xkcd_response['img']
    picture_extension = get_picture_extension(image_url)
    filename = f'comic{picture_extension}'
    download_comic(image_url, filename)

    logging.info('Получение комментария к картинке xkcd...')
    xkcd_comment = xkcd_response['alt']
    print(xkcd_comment)
    upload_response = upload_vk_picture(access_vk_token, group_id, filename)
    save_vk_picture(access_vk_token, group_id, upload_response)


