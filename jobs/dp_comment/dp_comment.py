# -*- coding:utf-8 -*-
__author__ = 'zhoujifeng'
__date__ = '2019/6/5 19:22'

import logging

import aiohttp

from setting.config import PROXY_DB
from utils.file_utils import FileUtils
from utils.catch_utils import CatchUtils
from utils.redis_utils import RedisUtils
from utils.async_func_utils import async_func_pool

logger = logging.getLogger('comment')


class Comment(object):
    def __init__(self, redis_db, redis_label='default'):
        history_cache = CatchUtils(RedisUtils.get_pool_by_label(redis_label, redis_db))

    def run(self):
        logger.info('开始获取读取本地地区文件')
        city_data = FileUtils.get_city()
        logger.info('开始获取商家评论数据')
        list(map(lambda x: self.crawler_start(x['code']), city_data['city'].values()))
        # pool = multiprocessing.Pool(processes=ProcessesNum)
        # for city in city_data['city'].values():
        #     pool.apply_async(cls.crawler_start, (city['code'],))
        #
        # pool.close()
        # pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束

    def crawler_start(self, city):
        pass
