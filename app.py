# -*- coding:utf-8 -*-
__author__ = 'zhoujifeng'
__date__ = '2019/6/5 19:18'

import logging
from logging.config import dictConfig

from jobs.proxy.proxy import Proxy
from setting.config import PROXIES_CONFIG
from utils.logger import LOGGING

logger = logging.getLogger('default')

if __name__ == '__main__':
    dictConfig(LOGGING)

    p = Proxy(**PROXIES_CONFIG)
    p.server()
