from datetime import datetime
import time

import sqlite3

from config import config
import parsing
from data import value_db


def data_update():

    value_db.check_db()

    while True:
        connect = sqlite3.connect(config.VALUE_SQL_FILENAME)
        cursor = connect.cursor()

        date_time = datetime.now()
        data = parsing.start_parsing()

        print(f'Дата:', date_time)
        print(f'Взял данные:', data)

        for x in data:
            print(f'Записываю в БД:', x)
            cursor.execute(
                'UPDATE main '
                'SET value=:value, time=:time '
                'WHERE unit=:unit ',
                {"unit": x, "value": data[x], "time": date_time}
            )

        connect.commit()

        cursor.close()
        connect.close()
        print('Жду 60 сек')
        time.sleep(600)
        print('Повторяю скрипт')
        continue
