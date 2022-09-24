with open('вк токен.txt', 'r') as file_object:
    vk_token = file_object.read().strip()
with open('яндекс диск токен.txt', 'r') as file_object:
    ya_token = file_object.read().strip()
import requests
from pprint import pprint
import time
from tqdm import tqdm
import json

def show_profile_photo(user_id, vk_token):
    url = "https://api.vk.com/method/photos.get"
    params = {
        "user_ids": user_id,
        "access_token": vk_token,
        "v": "5.131",
        "extended":"1",
        "album_id":"profile"
    }
    response = requests.get(url, params=params)
    res = response.json()
    all_info = res['response']['items']
    file_info = {} #словарь по каждому файлу отдельно
    files = [] #список всех файлов с нужной нам информацией
    likes = [] #список количества лайков на всех фото
    file_list = [] #создаем список для информации о каждом файле
    likes_res = [likes.append(like_counter['likes']['count']) for like_counter in all_info]
    for info_about_each in all_info:
        #разбираемся с именами файлов
        if likes.count(info_about_each['likes']['count'])==1:
            file_info = {'file_name':f"{info_about_each['likes']['count']}.jpg"}
        else:
            file_info = {'file_name': f"{info_about_each['likes']['count']} {info_about_each['date']}.jpg"}
        #выводим url каждого файла в лучшем качестве
        sizes = info_about_each['sizes']
        counted_sizes = [a['height'] * a['width'] for a in sizes]
        for el in sizes:
            if max(counted_sizes) == el['height']*el['width']:
                file_info.setdefault('url',el['url'])
                file_info.setdefault('size', el['type'])
                file_info.setdefault('date', info_about_each['date'])
                file_list.append(file_info)
                #добавляем все файлы в один список
                files.append(file_list)
    all_files_info = []
    for i in file_list:
        file_info_for_json = {'file_name': i['file_name']}
        file_info_for_json.setdefault('size', i['size'])
        all_files_info.append(file_info_for_json)
    DATA = {'items':all_files_info}

    with open('info.json', 'w', encoding='utf-8') as f:
        json.dump(DATA, f, indent=1)
    return files

def upload_files_to_YD(ya_token):
    headers = {
                "Authorization": f'OAuth {ya_token}',
                "Content-Type": "application/json"
            }
    params_for_folder = {
                "path": "/vk"
            }
    response_for_folder = requests.put("https://cloud-api.yandex.net/v1/disk/resources", headers=headers, params=params_for_folder, timeout=10)
    f_show_profile_photo = show_profile_photo('atsaregorodtseva', vk_token)
    for photos in f_show_profile_photo:
        pass
    number_of_photos = int(input("Количество фото для загрузки: "))
    for el in tqdm(photos[0:number_of_photos], desc= 'photo loading in progress'):
        path = el['url']
        file_name = el['file_name']
        params = {
                'url':path,
                'path':f"/vk/{file_name}'",
                'name': file_name,
                'overwrite':'false'
            }
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers, params=params, timeout=20)
        time.sleep(0.5)
    print('Uploading is finished')
show_profile_photo('atsaregorodtseva', vk_token)
upload_files_to_YD(ya_token)
