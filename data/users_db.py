import os
from datetime import date, timedelta

import sqlite3

from config import config


__DB = config.USERS_SQL_FILENAME


def init_db(connect, cursor):

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS stat ( "
        "date           TEXT, "
        "users          INT, "
        "new_users      INT, "
        "clicks         INT) "
        )

    connect.commit()

    minus_day = 89

    while minus_day >= 0:
        today = date.today() - timedelta(days=minus_day)
        cursor.execute(
            "INSERT INTO stat (date, users, new_users, clicks) VALUES (?, ?, ?, ?)", (today.strftime("%d.%m"), 0, 0, 0, )
        )
        minus_day -= 1

    connect.commit()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS user_id ( "
        "index          INTEGER PRIMARY KEY AUTOINCREMENT, "
        "id             INT, "
        "name           TEXT, "
        "username       TEXT, "
        "language       TEXT, "
        "first_visit    TEXT, "
        "last_visit     TEXT, "
        "visits_amount  INT, "
        "is_bot         BOOLEAN) "
    )

    connect.commit()


def is_db_exist():
    if not os.path.exists(__DB) or os.path.getsize(__DB) == 0:
        return False
    else:
        return True


def check_last_date_in_value_db(connect, cursor, today):
    cursor.execute(
        "SELECT date FROM stat WHERE rowid = 90"
    )
    last_date_in_db = cursor.fetchone()[0]
    print(last_date_in_db)

    if last_date_in_db != today:
        print("date update")
        cursor.execute("DELETE FROM stat WHERE rowid = 1")
        connect.commit()
        cursor.execute("INSERT INTO stat (date, users, new_users, clicks) VALUES (?, ?, ?, ?)", (today, 0, 0, 0, ))
        connect.commit()


def increase_value_in_value_db(what_value):
    connect = sqlite3.connect(__DB)
    cursor = connect.cursor()
    today = date.today().strftime("%d.%m")

    if not is_db_exist():
        init_db(connect, cursor)

    check_last_date_in_value_db(connect, cursor, today)

    cursor.execute(
        "SELECT %s FROM stat WHERE date=(?)" % what_value, (today, )
    )
    value_from_db = cursor.fetchone()[0]
    print(value_from_db)
    new_value = value_from_db + 1
    print(new_value)
    cursor.execute(
        "UPDATE stat SET %s=(?) WHERE date=(?)" % what_value, (new_value, today, )
    )
    connect.commit()

    cursor.close()
    connect.close()


def is_new_user(cursor, user):
    cursor.execute(
        "SELECT id FROM user_id WHERE id = (?)", (user.id, )
    )
    return cursor.fetchone()[0]


def add_new_user(connect, cursor, user, today):
    name = (user.first_name, user.last_name)
    print(user)
    print(name)
    print(today)

    cursor.execute(
        "INSERT INTO user_id "
        "(id, name, username, language, first_visit, last_visit, visits_amount, is_bot)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user.id, name, user.username, user.language_code, today, '-', 1, user.is_bot, )
    )
    connect.commit()

    increase_value_in_value_db('new_users')


def add_user_data(user):
    connect = sqlite3.connect(__DB)
    cursor = connect.cursor()
    today = date.today().strftime("%d.%m.%Y")

    if not is_db_exist():
        init_db(connect, cursor)

    if is_new_user(cursor, user):
        add_new_user(connect, cursor, user, today)
    else:
        cursor.execute(
            "SELECT visits_amount FROM user_id WHERE id = (?)", (user.id, )
        )

        increase_visits_amount = cursor.fetchone()[0] + 1

        cursor.execute(
            "UPDATE user_id "
            "SET (visits_amount, last_visit) "
            "VALUE (?, ?) "
            "WHERE id=(?)",
            (increase_visits_amount, today, user.id, )
        )
        connect.commit()

    cursor.close()
    connect.close()
