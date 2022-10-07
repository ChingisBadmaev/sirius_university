import requests
from bs4 import BeautifulSoup
import csv

URL ='https://music.yandex.ru/chart/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}
FILE = 'yandex_chart.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items_musics_names = soup.find_all('a', class_='d-track__title deco-link deco-link_stronger')
    musics_names = []
    for item in items_musics_names:
        data = item.get_text()[2:-2]    # [2:-2] т.к. в начале и в конце стоят два пробела
        musics_names.append(data)

    items_people_names = soup.find_all('span', class_='d-track__artists')
    people_names = []
    for item in items_people_names:
        data = item.get_text()
        people_names.append(data)
    return list(zip(musics_names, people_names))


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([
            'music_name', 'artist'])
        for item in items:
            writer.writerow([item[0], item[1]])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        save_file(get_content(html.text), FILE)
    else:
        print('Error')


parse()
