import aiohttp
from bs4 import BeautifulSoup
import requests
from Configs.config import header, home_url

from Modules.db_commnads import insert_genre, insert_autor, get_id_autor, get_id_genre, insert_music


async def check_url_img(url: str):
    try:
        if requests.get(url.replace("background-image: url('", "").replace("')", ""),
                        headers=header).status_code == 200:
            return url.replace("background-image: url('", "").replace("')", "")
        else:
            return None
    except:
        url = "https:" + url.replace("background-image: url('", "").replace("')", "")
        return url


async def check_url(url: str):
    try:
        if requests.get(url, headers=header).status_code == 200:
            return url
        else:
            return None
    except:
        return None


async def parse_genres(url: str) -> list:
    list_data: list = []
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=header)
        soup = BeautifulSoup(await response.text(), 'lxml')
        items = soup.find_all('li', class_='album-item')
        for item in items:
            genre_url = await check_url(url.replace('/genres', '') + item.find('a').get('href'))
            genre_img = await check_url_img(item.find('span', class_='album-image').get('style'))
            if genre_url is not None:
                data = {
                    'name': ' '.join(item.find('span', class_='album-title').text.replace('\n', '').split()),
                    'url': genre_url,
                    'img': genre_img if genre_img is not None else 'NULL'
                }
                insert_genre(data)
                list_data.append(data)
    return list_data


async def parse_tracks(l_url: list) -> None:
    async with aiohttp.ClientSession() as session:
        for url in l_url:
            response = await session.get(url=url, headers=header)
            soup = BeautifulSoup(await response.text(), 'lxml')
            b_page: str = ''.join([p.text for p in soup.find_all('a', class_='pagination__link') if p.text == '>'])
            c_page: str = ''.join(
                [p.get('href') for p in soup.find_all('a', class_='pagination__link') if p.text == '>'])
            pages: list = [home_url + c_page]
            while b_page == '>':
                resp = await session.get(url=home_url + c_page, headers=header)
                parce_page = BeautifulSoup(await resp.text(), 'lxml')
                b_page = ''.join([p.text for p in parce_page.find_all('a', class_='pagination__link') if p.text == '>'])
                c_page = ''.join(
                    [p.get('href') for p in parce_page.find_all('a', class_='pagination__link') if p.text == '>'])
                pages.append(home_url + c_page)
            for page in pages:
                response = await session.get(url=page, headers=header)
                soup = BeautifulSoup(await response.text(), 'lxml')
                items = soup.find_all('li', class_='tracks__item')
                for item in items:
                    print(item.find('div', class_='track__desc').text)
                    insert_autor(item.find('div', class_='track__desc').text)
                    try:
                        insert_music(
                            {
                                'name': ' '.join(item.find('div', class_='track__title').text.replace('\n', '').split()),
                                'autor': get_id_autor(item.find('div', class_='track__desc').text),
                                'genre': get_id_genre(url),
                                'img': item.find('div', class_='track__img').get('style'). \
                                    replace("background-image: url('", "").replace("');", ""),
                                'url': item.find('a', class_='track__download-btn').get('href'),
                                'time': item.find('div', class_='track__fulltime').text
                            }
                        )
                    except Exception:
                        raise Exception
