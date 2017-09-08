# __author: Lambert
# __date: 2017/9/6 17:48
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': '%s/db/' % BASE_DIR
}
DB_PATH = '%s/%s/' % (DATABASE['path'], DATABASE['name'])

LOG_PATH = '%s/%s/' % (BASE_DIR, 'log')
LOG_LEVEL = logging.INFO
LOG_TYPE = {
    'transactions': 'transactions.log',
    'access': 'access.log'
}
