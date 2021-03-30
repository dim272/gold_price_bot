import os
from datetime import date, timedelta

import sqlite3

from config import config


__DB = config.USERS_SQL_FILENAME


def init_stat_db(connect, cursor):
    print('Инициализируем таблицу stat в users.db')

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


def init_users_total_db(connect, cursor):
    print('Инициализируем таблицу users_total в users.db')

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


def init_users_today_db(connect, cursor):
    print('Инициализируем таблицу users_today в users.db')

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users_today ( "
        "id             INTEGER PRIMARY KEY AUTOINCREMENT, "
        "user_id        INT, "
        "date           TEXT) "
    )

    connect.commit()


def is_users_db_exist():
    print('Проверяем существование users.db')

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
    print('Проверяем последнюю дату в stat > users.db')

    cursor.execute(
        "SELECT date FROM stat WHERE rowid = 90"
    )
    last_date_in_stat_db = cursor.fetchone()[0]
    print('Последняя дата в stat > users_id.db', last_date_in_stat_db)

    if last_date_in_stat_db != today:
        print('Обновляем последнюю дату в stat > users.db на', today)

        cursor.execute("DELETE FROM stat WHERE rowid = 1")
        connect.commit()
        cursor.execute("INSERT INTO stat (date, users, new_users, clicks) VALUES (?, ?, ?, ?)", (today, 0, 0, 0, ))
        connect.commit()


def increase_value_in_stat_db(what_value):
    print('Увеличиваем значение', what_value, 'в stat > users.db')

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

    print('Значение', value_from_db, 'изменено на', new_value, 'в stat > users.db')

    cursor.close()
    connect.close()


def check_date_in_users_today_db(connect, cursor, today):
    is_date_updated = True

    print('Проверяем последнюю дату в users_today > users.db')

    cursor.execute(
        "SELECT date FROM users_today WHERE rowid = 1"
    )
    last_date_in_users_today_db = cursor.fetchone()
    print('Последняя дата в users_today > users_id.db', last_date_in_users_today_db)

    if last_date_in_users_today_db != today:
        print('Обновляем последнюю дату в users_today > users.db на', today)

        cursor.execute("DELETE FROM users_today")
        connect.commit()

        is_date_updated = True

    return is_date_updated


def is_new_user_in_users_today_db(cursor, user):
    print('Ищем пользователя в записях users_today > users.db')

    cursor.execute(
        "SELECT user_id FROM users_today WHERE user_id = (?)", (user.id,)
    )
    x = cursor.fetchone()
    print("Результат поиска:", x)
    return x


def add_user_in_users_today_db(user):
    print('Начинаем добавление данных пользователя в users_today > users.db')

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
    print('Ищем пользователя в записях users_total > users.db')

    cursor.execute(
        "SELECT user_id FROM users_total WHERE user_id = (?)", (user.id, )
    )

    return cursor.fetchone()


def add_new_user_in_users_total_db(connect, cursor, user, today):
    print('Добавляем данные нового пользователя в users_total > users.db')

    name = (user.first_name + " " + user.last_name)

    cursor.execute(
        "INSERT INTO users_total "
        "(user_id, name, username, language, first_visit, last_visit, visits_amount, is_bot) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user.id, name, user.username, user.language_code, today, '-', '1', user.is_bot, )
    )
    connect.commit()

    print(f'\n'
          f'В user_id > users.db добавлен новый пользователь с данными:\n'
          f'user id: {user.id}\n'
          f'name: {name}\n'
          f'username: {user.username}\n'
          f'language: {user.language_code}\n'
          f'first_visit: {today}\n'
          f'last_visit: -\n'
          f'visits_amount: 1\n'
          f'is_bot: {user.is_bot}\n')

    print('Даём задание увеличить переменную "new_users" в stat > users.db')

    increase_value_in_stat_db('new_users')


def add_user_data_in_users_total_db(user):
    print('Начинаем добавление данных пользователя в users_total > users.db')

    connect = sqlite3.connect(__DB)
    cursor = connect.cursor()
    today = date.today().strftime("%d.%m.%Y")

    if not is_table_in_users_db_exist(cursor, 'users_total'):
        init_users_total_db(connect, cursor)

    if not is_new_user_in_users_total_db(cursor, user):
        print('Пользователь не найден в users_total > users.db\n'
              'Даём задание добавить данные нового пользователя')

        add_new_user_in_users_total_db(connect, cursor, user, today)

    else:
        print('Пользователь найден в users_total > users.db\n'
              'Даём задание обновить данные количества посещений и даты последнего визита пользователя')

        cursor.execute(
            "SELECT visits_amount FROM users_total WHERE user_id = (?)", (user.id, )
        )
        visits_amount = cursor.fetchone()[0]
        print(visits_amount)
        increase_visits_amount = visits_amount + 1
        print(increase_visits_amount)

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