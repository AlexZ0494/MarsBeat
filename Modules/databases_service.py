import sqlite3


class Config:
    def __init__(self, path='user_database.db'):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.create_tables()

    def db_select(self, query: str) -> list:
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.con.rollback()
        self.cur.close()
        return result

    def db_commit(self, query: str) -> bool:
        try:
            self.cur.execute(query)
            self.con.commit()
            self.cur.close()
            return True
        except Exception as e:
            print("Error executing: ", str(e))
            return False

    # def db_insert(self, table_name: str, columns: list, data: dict):
    #     self.cur.execute(f'''INSERT INTO {table_name} ({", ".join(columns)})
    #     values ('{"', '".join(data.values())}')''')
    #     self.con.commit()
    #     self.cur.close()
    #
    # def db_update(self, table_name: str, column: str, data, where: str):
    #     self.cur.execute(f'UPDATE {table_name} SET {column} = {data} WHERE {where}')
    #     self.con.commit()
    #     self.cur.close()
    #
    # def db_remove(self):
    #     ...

    def get_columns(self, table_name: str) -> list:
        items = self.cur.execute(table_name)
        return [item[0] for item in items.description]

    def create_tables(self):
        with open("Requests/create_table_genres.sql", "r") as f_o:
            self.cur.executescript(f_o.read())
    #
    # def selected_urls_genres(self):
    #     query = '''SELECT id, url FROM GENRES'''
    #     self.cur.execute(query)
    #     return self.cur.fetchall()
    #
    # def selected_ids_genres(self, url: str):
    #     query = f"SELECT id FROM GENRES WHERE url = '{url}'"
    #     self.cur.execute(query)
    #     return self.cur.fetchone()[0]
    #
    # def insert_author(self, data: str) -> bool:
    #     try:
    #         query = f"""INSERT OR IGNORE INTO AUTOR (name) values ('{data}')"""
    #         self.cur.execute(query)
    #         self.con.commit()
    #         return True
    #     except Exception as error:
    #         print(f'Error inserting: {error}')
    #         return False
    #
    # def insert_music(self, data: tuple) -> bool:
    #     try:
    #
    #         query = """INSERT INTO MUSIC (name, id_autor, id_genre, file, img)  VALUES (?, ?, ?, ?, ?)"""
    #         self.cur.execute(query, data)
    #         self.con.commit()
    #         return True
    #     except Exception as error:
    #         print(f'Error inserting: {error}')
    #         return False
