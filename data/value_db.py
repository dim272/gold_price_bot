import os
from datetime import datetime

import sqlite3

from config import config
import parsing


__CONNECT = None
__DB = config.VALUE_SQL_FILENAME


def connection():
    global __CONNECT
    if __CONNECT is None:
        __CONNECT = sqlite3.connect(__DB)
    return __CONNECT


def init_db():
    connect = connection()
    cursor = connect.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS main ( "
        "unit        TINYTEXT,"
        "value       FLOAT,"
        "time        TEXT )"
        )

    connect.commit()

    date_time = datetime.now()
    data = parsing.start_parsing()

    for x in data:
        cursor.execute(
            "INSERT INTO main (unit, value, time) VALUES (?, ?, ?)",
            (x, data[x], date_time)
        )
    connect.commit()

    cursor.close()
    connect.close()


def check_db():
    if not os.path.exists(__DB) or os.path.getsize(__DB) == 0:
        init_db()


def read(val):
    connect = connection()
    cursor = connect.cursor()
    cursor.execute('SELECT value FROM main WHERE unit=:unit', {"unit": val})
    result = cursor.fetchone()
    cursor.close()
    return result[0]
