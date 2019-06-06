# -*- coding:utf-8 -*-
import logging

from jobs.proxy.proxy import Proxy
from setting.config import PROXY_DB, PROXIES_CONFIG

__author__ = 'zhoujifeng'
__date__ = '2019/6/5 19:18'

from logging.config import dictConfig

from utils.logger import LOGGING
logger = logging.getLogger('default')

if __name__ == '__main__':
    dictConfig(LOGGING)

    p = Proxy(redis_db=PROXY_DB, **PROXIES_CONFIG)
    p.server()