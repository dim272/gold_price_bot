import os.path
import datetime
import json

from config import DB_FILENAME
from parsing import start_parsing


def get_data():
    if os.path.exists(DB_FILENAME) is True:
        today = datetime.datetime.today()
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(DB_FILENAME))
        duration = today - modified_date
        if duration.seconds >= 3600 and os.path.getsize(DB_FILENAME) == 0:
            start_parsing()
    else:
        start_parsing()

    data = read_data_from_datafile()
    return data


def read_data_from_datafile():
    with open(DB_FILENAME, 'r') as f:
        value = json.loads(f.readline())
    return value