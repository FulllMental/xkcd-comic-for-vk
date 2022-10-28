import logging
import os
from random import randint
from urllib.parse import unquote, urlsplit

import requests
from dotenv import load_dotenv


def upload_vk_picture(access_vk_token, group_id, filename):

    logging.info('Загрузка картинки на сервер VK...')
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

    logging.info('Сохранение картинки в альбом...')
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
    return response.json()


def post_vk_picture(save_vk_picture_response, xkcd_comment):

    logging.info('Публикую картинку и пост в группу...')
    url = 'https://api.vk.com/method/wall.post'
    picture_id = save_vk_picture_response["response"][0]["id"]
    owner_id = save_vk_picture_response["response"][0]["owner_id"]
    payload = {
        'access_token': access_vk_token,
        'v': 5.131,
        'group_id': group_id,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{picture_id}',
        'message': xkcd_comment,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()


def get_xkcd_random_response():

    logging.info('Получение ответа от xkcd...')
    first_response = requests.get('https://xkcd.com/info.0.json')
    first_response.raise_for_status()
    total_pictures = first_response.json()['num']
    comic_number = randint(0, total_pictures)
    response = requests.get(f'https://xkcd.com/{comic_number}/info.0.json')
    response.raise_for_status()
    return response.json()


def get_picture_extension(image_url):

    logging.info('Выделение расширения файла...')
    link_split = urlsplit(image_url)
    file_name = unquote(link_split[2])
    file_extension = os.path.splitext(file_name)
    return file_extension[1]


def download_xkcd_comic(image_url, filename):

    logging.info('Скачивание картинки...')
    response = requests.get(image_url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    load_dotenv()
    access_vk_token = os.getenv('ACCESS_VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    logging.basicConfig(level=logging.INFO)

    xkcd_response = get_xkcd_random_response()
    image_url = xkcd_response['img']
    picture_extension = get_picture_extension(image_url)
    filename = f'comic{picture_extension}'
    download_xkcd_comic(image_url, filename)

    logging.info('Получение комментария к картинке xkcd...')
    xkcd_comment = xkcd_response['alt']
    upload_response = upload_vk_picture(access_vk_token, group_id, filename)
    save_vk_picture_response = save_vk_picture(access_vk_token, group_id, upload_response)
    post_vk_picture(save_vk_picture_response, xkcd_comment)
    os.remove(filename)

