# __author: Lambert
# __date: 2017/9/7 17:10
import logging
from conf import setting


def log(logo_type):
    logger = logging.getLogger(logo_type)

    formater = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    formater.datefmt = "%Y-%m-%d %H:%M:%S"

    fh = logging.FileHandler('%s%s' % (setting.LOG_PATH, setting.LOG_TYPE[logo_type]), encoding='utf8')
    ch = logging.StreamHandler()
    fh.setFormatter(formater)
    ch.setFormatter(formater)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.setLevel(setting.LOG_LEVEL)
    return logger
