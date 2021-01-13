import os.path, datetime
import json


class NewUser:

    user_count = 0

    def __init__(self):
        self.today = datetime.datetime.today()
        self.bd_file_name = 'datafile'
        self.statistic_file_name = 'stat'
        self.data1 = self.get_data()
        NewUser.user_count += 1

    def get_data(self):
        self.today = datetime.datetime.today()
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(self.bd_file_name))
        duration = self.today - modified_date
        if os.path.exists(self.bd_file_name) is True and duration.seconds <= 3600 and os.path.getsize(self.bd_file_name) > 0:
            data = self.read_data_from_datafile()
        else:
            from parsing import start_parsing
            start_parsing()
            data = self.read_data_from_datafile()
        return data

    def read_data_from_datafile(self):
        with open(self.bd_file_name, 'r') as f:
            value = json.loads(f.readline())
        return value

    def probe(self, val):
        result = self.data[0]*val
        return result

    def write_statistic(self):
        pass


if __name__ == "__main__":
    print('main')
