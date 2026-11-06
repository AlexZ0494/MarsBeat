from Modules.databases_service import Config


def insert_genre(data: dict) -> None:
    query = f"""INSERT INTO GENRES (name, url, img)
    VALUES ('{data.get('name')}', '{data.get('url')}', '{data.get('img')}')"""
    Config().db_commit(query)


def add_update_favorite_genres(data: list) -> None:
    for item in data:
        query = f"""UPDATE GENRES SET favorite = 1 WHERE name = '{item['name']}' and url = '{item['url']}'"""
        Config().db_commit(query)


def get_all_genres() -> list:
    result: list = []
    query: str = "SELECT * FROM GENRES"
    items: list = Config().db_select(query)
    attrs: list = Config().get_columns(query)
    for item in items:
        dictionary: dict = {}
        for attr in enumerate(attrs):
            dictionary.setdefault(attr[1], item[attr[0]])
        result.append(dictionary)
    return result


def get_favorites_genres() -> list:
    result: list = []
    query: str = "SELECT * FROM GENRES WHERE FAVORITE is TRUE"
    items: list = Config().db_select(query)
    attrs: list = Config().get_columns(query)
    for item in items:
        dictionary: dict = {}
        for attr in enumerate(attrs):
            dictionary.setdefault(attr[1], item[attr[0]])
        result.append(dictionary)
    return result


def get_id_autor(name: str) -> str:
    query = f"""SELECT id FROM AUTOR WHERE name = '{name}'"""
    return Config().db_select(query)[0][0]


def insert_autor(name: str) -> None:
    query = f"""INSERT OR IGNORE INTO AUTOR (name) VALUES ("{name}")"""
    Config().db_commit(query)


def get_id_genre(url: str) -> str:
    query = f"""SELECT id FROM GENRES WHERE url='{url}'"""
    return Config().db_select(query)[0][0]


def insert_music(data: dict):
    query = f'''INSERT INTO MUSIC (name, id_autor, id_genre, file, img, _time)
    VALUES ("{data.get('name')}", "{data.get('autor')}", "{data.get('genre')}", "{data.get('url')}", 
    "{data.get('img')}", "{data.get('time')}")
    ON CONFLICT(name) 
    DO UPDATE SET file="{data.get('url')}", img="{data.get('img')}", _time="{data.get('time')}"'''
    Config().db_commit(query)


def get_music() -> list:
    result: list = []
    query: str = "SELECT * FROM MUSIC ORDER BY id_genre"
    items: list = Config().db_select(query)
    attrs: list = Config().get_columns(query)
    for item in items:
        dictionary: dict = {}
        for attr in enumerate(attrs):
            dictionary.setdefault(attr[1], item[attr[0]])
        result.append(dictionary)
    return result


def get_rand_music() -> list:
    result: list = []
    query: str = "SELECT m.name, a.name as autor, m.file, m.img, _time FROM MUSIC m, AUTOR a WHERE m.id_autor = a.id " \
                 "ORDER BY RANDOM() LIMIT 100"
    items: list = Config().db_select(query)
    attrs: list = Config().get_columns(query)
    for item in items:
        dictionary: dict = {}
        for attr in enumerate(attrs):
            dictionary.setdefault(attr[1], item[attr[0]])
        result.append(dictionary)
    return result
