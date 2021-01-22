import os.path
import datetime
import json

import requests
from bs4 import BeautifulSoup
import config


def get_data():
    if os.path.exists(config.DB_FILENAME) is True:
        today = datetime.datetime.today()
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(config.DB_FILENAME))
        duration = today - modified_date
        if duration.seconds >= 600 or os.path.getsize(config.DB_FILENAME) == 0:
            start_parsing()
    else:
        start_parsing()

    data = read_data_from_datafile()
    return data


def read_data_from_datafile():
    with open(config.DB_FILENAME, 'r') as f:
        value = json.loads(f.readline())
    return value


def start_parsing():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 '
                      'Safari/537.36'}

    page_gold = requests.get(config.GOLD_URL, headers=headers)
    soup_gold = BeautifulSoup(page_gold.content, 'html.parser')

    oz_usd = float(
        soup_gold.find('span', {'class': 'chart__info__sum'}).text.replace(' ', '').replace('$', '').replace(',', '.'))

    page_usd = requests.get(config.USD_URL, headers=headers)
    soup_usd = BeautifulSoup(page_usd.content, 'html.parser')

    usd = float(
        soup_usd.find('span', {'class': 'chart__info__sum'}).text.replace(' ', '').replace('₽', '').replace(',', '.'))

    gr_999_usd = round(float(oz_usd / 31.1), 2)
    gr_999_rub = int((oz_usd * usd) / 31.1)
    gr_958_rub = int(gr_999_rub * 0.958)
    gr_900_rub = int(gr_999_rub * 0.9)
    gr_850_rub = int(gr_999_rub * 0.85)
    gr_750_rub = int(gr_999_rub * 0.75)
    gr_585_rub = int(gr_999_rub * 0.585)
    gr_500_rub = int(gr_999_rub * 0.5)
    gr_375_rub = int(gr_999_rub * 0.375)
    gr_333_rub = int(gr_999_rub * 0.333)

    data_massive = {'oz_usd': oz_usd, 'gr_999_usd': gr_999_usd, 'gr_999_rub': gr_999_rub, 'gr_958_rub': gr_958_rub,
                    'gr_900_rub': gr_900_rub, 'gr_850_rub': gr_850_rub, 'gr_750_rub': gr_750_rub,
                    'gr_585_rub': gr_585_rub, 'gr_500_rub': gr_500_rub, 'gr_375_rub': gr_375_rub,
                    'gr_333_rub': gr_333_rub}

    with open(config.DB_FILENAME, 'w') as f:
        f.write(json.dumps(data_massive))
