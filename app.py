# -*- coding:utf-8 -*-
__author__ = 'zhoujifeng'
__date__ = '2019/6/5 19:18'

from logging.config import dictConfig

from utils.logger import LOGGING

if __name__ == '__main__':
    dictConfig(LOGGING)
