import os
from datetime import datetime, time

import sqlite3

from config import config
import parsing


__DB = config.VALUE_SQL_FILENAME


def init_db(connect, cursor):

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


def is_value_db_data_updated(cursor):

    data_updated = True

    cursor.execute("SELECT time FROM main WHERE unit='gr_999_rub'")

    last_update_value_db = cursor.fetchone()[0]
    then = datetime.strptime(last_update_value_db, '%Y-%m-%d %H:%M:%S.%f').timestamp()
    now = datetime.now().timestamp()
    seconds_passed = now - then

    if seconds_passed >= 600:
        data_updated = False

    return data_updated


def update_value_db(connect, cursor):

    date_time = datetime.now()
    data = parsing.start_parsing()

    for x in data:
        cursor.execute(
            'UPDATE main '
            'SET value=:value, time=:time '
            'WHERE unit=:unit ',
            {"unit": x, "value": data[x], "time": date_time}
        )

    connect.commit()


def is_value_db_exist():

    if not os.path.exists(__DB) or os.path.getsize(__DB) == 0:
        return False
    else:
        return True


def read_value_db(val):

    connect = sqlite3.connect(__DB)
    cursor = connect.cursor()

    if not is_value_db_exist():
        init_db(connect, cursor)

    if not is_value_db_data_updated(cursor):
        update_value_db(connect, cursor)

    cursor.execute('SELECT value FROM main WHERE unit=:unit', {"unit": val})
    result = cursor.fetchone()[0]

    cursor.close()
    connect.close()

    return result
