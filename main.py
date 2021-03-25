# Task1 Работа с SuperHero API (https://superheroapi.com/?ref=apilist.fun#appearance).
# Нужно определить кто самый умный(intelligence) из трех супергероев - Hulk, Captain America, Thanos.


import requests

def compare_heroes(heroes):
  my_dict = dict()
  best_iq = 0
  for name in heroes:
    url = "https://superheroapi.com/api/2619421814940190/search/" + name
    resp = requests.get(url, timeout=5).json()
    for item in resp['results']:
      if item['name'] == name:
        temp_dict = dict()
        temp_dict['name'] = name
        # temp_dict['id'] = item['id']  # дополн. информация о герое
        temp_dict['intelligence'] = item['powerstats']['intelligence']
        if best_iq < int(temp_dict['intelligence']):
          best_iq = int(temp_dict['intelligence'])
        my_dict[name] = temp_dict
  for key, value in my_dict.items():
    if int(value['intelligence']) == best_iq:
        resp = f"Самый умный супергерой: {value['name']}"
  return resp

if __name__ == '__main__':
  heroes = ['Hulk', 'Captain America', 'Thanos']
  print(compare_heroes(heroes))


# Task2 Работа с Яндекс.Диск API (Полигон - https://yandex.ru/dev/disk/poligon/).
# Нужно написать программу, которая принимает на вход путь до файла на компьютере и сохраняет на Яндекс.Диск с таким же именем.


class YaUploader:
    
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, disk_file_path, filename):
        """Метод загруджает файл file_path на яндекс диск"""
        href = self._get_upload_link(disk_file_path=disk_file_path).get('href', '')
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            message = f'\nФайл "{disk_file_path}" успешно загружен на Ваш Яндекс.Диск!'
        return print(message)


if __name__ == '__main__':
    uploader = YaUploader('<YourToken>')
    result = uploader.upload('file.txt', r'c:\my_folder\file.txt')
