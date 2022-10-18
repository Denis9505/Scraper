import json
from bs4 import BeautifulSoup
import requests


url_1 = 'https://oriencoop.cl/sucursales.htm'


URL = requests.get(url_1).text
soup = BeautifulSoup(URL, 'lxml')


def save_json(data):
    with open('storage.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_list_city_links(soup):
    data = soup.find('ul', class_='c-list c-accordion').find_all('a')
    urls_raw = [url.get('href') for url in data if 'sucursales' in url.get("href")]
    urls = []
    for url in urls_raw:
        res = f'https://oriencoop.cl'+url
        urls.append(res)
    return urls


def get_data(soup):
 
    all_data = soup.find('div', class_='s-dato')
    name = all_data.contents[1].text
    address = all_data.find('span').text
    phones = all_data.find_all('span')[1].string
    working_hours = [res.text for res in all_data.find_all('p')[-1]]
    working_hours[:] = [n for n in working_hours if n.strip()]
    return {
            'address': address,
            'latlon': '',
            'name': name,
            'phones': [phones, ],
            'working_hours': working_hours
        }


def get_all_data(soup) -> list:
    clear_data = []
    for link in get_list_city_links(soup):
        url_link = requests.get(link).text
        soup = BeautifulSoup(url_link, 'lxml')
        data = get_data(soup)
        clear_data.append(data)
        save_json(clear_data)

if __name__ == '__main__':
    get_all_data(soup)
