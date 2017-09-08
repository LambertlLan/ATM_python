# __author: Lambert
# __date: 2017/9/6 14:54
import time
from core import db_handler


def login_required(func):
    def wrap(*args, **kwargs):
        if args[0]['is_authenticated']:
            return func(*args, **kwargs)
        else:
            exit("User is not authenticated.")

    return wrap


def check_db(usr, pwd):
    data = db_handler.read_data(usr)
    if data and data['password'] == pwd:
        exp_time_stamp = time.mktime(time.strptime(data['expire_date'], '%Y-%m-%d'))
        if exp_time_stamp > time.time():
            return data
        else:
            print('账户已过期！')
    else:
        print('用户名或密码错误')


def login(user_data, logger):
    retry_count = 0
    while user_data['is_authenticated'] is not True and retry_count < 3:
        username = input("\033[32;1maccount:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        login_status = check_db(username, password)
        if login_status:
            user_data['is_authenticated'] = True
            user_data['account_id'] = login_status['id']
            logger.info(u'登录成功')
            return login_status
        retry_count += 1
    else:
        logger.error('尝试次数过多')
        exit()
