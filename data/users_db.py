import os
from datetime import date, timedelta

import sqlite3

from config import config

# users.db CONTROL
# if something goes wrong look at bot.log

__DB = config.USERS_SQL_FILENAME

# Initialize table "stat"
# where we will record data on:
# the daily number of users         - users
# the daily number of new users     - new_users
# the daily number of requests      - clicks


def init_stat_db(connect, cursor):

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


# Initialize table "users_total"
# where we will write data about each new user

def init_users_total_db(connect, cursor):

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users_total ( "
        "id             INTEGER PRIMARY KEY AUTOINCREMENT, "
        "user_id        INT, "
        "name           TEXT, "
        "username       TEXT, "
        "language       TEXT, "
        "first_visit    TEXT, "
        "last_visit     TEXT, "
        "visits_amount  INT, "
        "is_bot         BOOLEAN) "
    )

    connect.commit()


# Initialize table "users_today"
# this will tell us the number of unique users

def init_users_today_db(connect, cursor):

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users_today ( "
        "user_id        INT, "
        "date           TEXT) "
    )

    connect.commit()


def is_users_db_exist():

    if not os.path.exists(__DB) or os.path.getsize(__DB) == 0:
        return False
    else:
        return True


def is_table_in_users_db_exist(cursor, table_name):
    if is_users_db_exist():
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = (?)", (table_name, )
            )
        return cursor.fetchone()


def check_last_date_in_stat_db(connect, cursor, today):
    cursor.execute(
        "SELECT date FROM stat WHERE rowid = 91"
    )
    last_date_in_stat_db = cursor.fetchone()

    if last_date_in_stat_db:
        if last_date_in_stat_db != today:
            print('Обновляю дату')

            cursor.execute("DELETE FROM stat WHERE rowid = 2")
            connect.commit()
            cursor.execute("INSERT INTO stat (date, users, new_users, clicks) VALUES (?, ?, ?, ?)", (today, 0, 0, 0, ))
            connect.commit()

        cursor.execute(
            "SELECT Count(*) FROM stat"
        )
        row_count = cursor.fetchone()


def increase_value_in_stat_db(what_value):

    connect = sqlite3.connect(__DB)
    cursor = connect.cursor()
    today = date.today().strftime("%d.%m")

    if not is_table_in_users_db_exist(cursor, 'stat'):
        init_stat_db(connect, cursor)
    else:
        check_last_date_in_stat_db(connect, cursor, today)

    cursor.execute(
        "SELECT %s FROM stat WHERE date=(?)" % what_value, (today, )
    )
    value_from_db = cursor.fetchone()[0]
    new_value = value_from_db + 1
    cursor.execute(
        "UPDATE stat SET %s=(?) WHERE date=(?)" % what_value, (new_value, today, )
    )
    connect.commit()

    cursor.close()
    connect.close()


def check_date_in_users_today_db(connect, cursor, today):
    is_date_updated = True

    cursor.execute(
        "SELECT date FROM users_today WHERE rowid = 1"
    )
    last_date_in_users_today_db = cursor.fetchone()

    if last_date_in_users_today_db:
        if last_date_in_users_today_db[0] != today:

            cursor.execute("DELETE FROM users_today")
            connect.commit()

            is_date_updated = True

    return is_date_updated


def is_new_user_in_users_today_db(cursor, user):

    cursor.execute(
        "SELECT user_id FROM users_today WHERE user_id = (?)", (user.id,)
    )
    x = cursor.fetchone()

    return x


def add_user_in_users_today_db(user):

    connect = sqlite3.connect(__DB)
    cursor = connect.cursor()

    init_users_today_db(connect, cursor)

    today = date.today().strftime("%d.%m.%Y")

    if check_date_in_users_today_db(connect, cursor, today):
        if not is_new_user_in_users_today_db(cursor, user):
            cursor.execute(
                "INSERT INTO users_today "
                "(user_id, date) "
                "VALUES (?, ?)",
                (user.id, today, )
            )
            connect.commit()
            increase_value_in_stat_db('users')
    else:
        cursor.execute(
            "INSERT INTO users_today "
            "(user_id, date) "
            "VALUES (?, ?)",
            (user.id, today,)
        )
        connect.commit()
        increase_value_in_stat_db('users')

    cursor.close()
    connect.close()


def is_new_user_in_users_total_db(cursor, user):

    cursor.execute(
        "SELECT user_id FROM users_total WHERE user_id = (?)", (user.id, )
    )

    return cursor.fetchone()


def add_new_user_in_users_total_db(connect, cursor, user, today):

    name = (user.first_name + " " + user.last_name)

    cursor.execute(
        "INSERT INTO users_total "
        "(user_id, name, username, language, first_visit, last_visit, visits_amount, is_bot) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user.id, name, user.username, user.language_code, today, '-', '1', user.is_bot, )
    )
    connect.commit()

    increase_value_in_stat_db('new_users')


def add_user_data_in_users_total_db(user):

    connect = sqlite3.connect(__DB)
    cursor = connect.cursor()
    today = date.today().strftime("%d.%m.%Y")

    if not is_table_in_users_db_exist(cursor, 'users_total'):
        init_users_total_db(connect, cursor)

    if not is_new_user_in_users_total_db(cursor, user):

        add_new_user_in_users_total_db(connect, cursor, user, today)

    else:
        init_users_today_db(connect, cursor)
        if not is_new_user_in_users_today_db(cursor, user):

            cursor.execute(
                "SELECT visits_amount FROM users_total WHERE user_id = (?)", (user.id, )
            )
            visits_amount = cursor.fetchone()[0]
            increase_visits_amount = visits_amount + 1

            cursor.execute(
                "UPDATE users_total "
                "SET visits_amount=(?), last_visit=(?) "
                "WHERE user_id=(?)",
                (increase_visits_amount, today, user.id, )
            )
            connect.commit()

    cursor.close()
    connect.close()


def check_user(user):
    add_user_data_in_users_total_db(user)
    add_user_in_users_today_db(user)