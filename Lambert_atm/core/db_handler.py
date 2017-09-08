# __author: Lambert
# __date: 2017/9/7 14:34
import json
import os
from conf import setting


def update_data(data):
    file_path = '%s/%s.json' % (setting.DB_PATH, data['id'])
    if os.path.isfile(file_path):
        with open(file_path, 'w') as update_file:
            json.dump(data, update_file)
            return True
    else:
        print('no such file')
        return False


def read_data(id):
    file_path = '%s/%s.json' % (setting.DB_PATH, id)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as read_file:
            data = json.load(read_file)
            return data
    else:
        print('no such file')
        return False


def read_log(log_type):
    file_path = '%s%s' % (setting.LOG_PATH, setting.LOG_TYPE[log_type])
    with open(file_path, 'r', encoding='utf8') as log_file:
        print(log_file.read())
