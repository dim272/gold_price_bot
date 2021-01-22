import sqlite3
import config
import parsing


class DB:
    def __init__(self):
        self.connect = sqlite3.connect(config.DB_FILENAME)
        self.cursor = self.connect.cursor()
        self.create()
        self.data = parsing.get_data()

    def create(self):
        try:
            self.cursor.execute(
                f"CREATE TABLE gold"
                "(usd REAL, gold REAL, 999 REAL,"
                "958 REAL, 900 REAL, 850 REAL, 750 REAL, "
                "585 REAL, 500 REAL, 375 REAL, 333 REAL")

            print('Создана база gold')
            self.connect.commit()

        except sqlite3.Error:
            print(sqlite3.Error)

        finally:
            self.cursor.close()
            print('После создания соединение закрыто')

    def write(self):
        print('Записываем значение')
        self.cursor.execute(f"INSERT INTO gold VALUES({self.data})")
        self.connect.commit()

    def read(self, val):
        self.cursor.execute(f'SELECT {val} FROM employees')


data = DB
print(data)
data.create()
