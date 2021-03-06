# -*- coding:utf-8 -*-
from datetime import datetime

__author__ = 'zhoujifeng'
__date__ = '2019/6/5 19:59'

import logging
import time
from logging.config import dictConfig

import requests

from setting.config import PROXIES_CONFIG, PROXY_DB
from utils.catch_utils import CatchUtils
from utils.logger import LOGGING
from utils.redis_utils import RedisUtils

logger = logging.getLogger('proxy')


class Proxy:
    def __init__(self, api_url, pool_size, time_out, redis_db, sleep, batch, redis_label='default'):
        logger.info('[Proxy]开始初始化......')
        self.__api_url = api_url
        self.__pool_size = pool_size
        self.__time_out = time_out
        self.__batch = batch
        self.__session = requests.Session()
        self.__init_session__()
        self.sleep = sleep

        self.catch = CatchUtils(RedisUtils.get_pool_by_label(redis_label, redis_db))

    def server(self):
        while True:
            logger.info('代理池维护服务开始运行...')
            db_size = self.catch.dbsize()
            logger.info('当前代理池长度为:%d' % (db_size,))

            if db_size >= self.__pool_size:
                logger.info('代理池不需要更新,休眠1秒')
                time.sleep(1)
                continue
            diff_size = self.__pool_size - db_size
            if diff_size <= 0:
                continue
            if diff_size < self.__batch:
                length = diff_size
            else:
                length = self.__batch

            data = self.get(length)
            if data:
                self.set(data)
                diff_size -= self.__batch
            logger.info('开始休眠:%.2f秒' % (self.sleep,))
            time.sleep(self.sleep)

    def __init_session__(self):
        logger.info('[requests]开始初始化')
        self.__session.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Connection": "close"
        }
        self.__session.keep_alive = False  # 关闭多余连接

    def get(self, length):
        url = self.__api_url.format(length)
        try:
            req = self.__session.get(url)
            logger.info('开始请求:[%s]' % (req.url,))
            req.raise_for_status()
            data = req.text
            req.close()
            return data

        except Exception as e:
            logger.error(e)
            logger.error('代理请求失败')
            return None

    def set(self, data):
        """
        向redis中添加代理ip
        :param data:
        :return:
        """
        logger.info('开始更新代理ip')
        proxies_dict = dict(map(lambda x: [x, str(datetime.now())], data.strip('\r\n').split('\r\n')))
        self.catch.mset(proxies_dict, timeout=self.__time_out)
        logger.info('代理ip更新完成')

        # list(map(lambda x: self.catch.set(key=x[0], value=x[1], timeout=self.__time_out), proxies_dict.items()))


if __name__ == '__main__':
    dictConfig(LOGGING)
    p = Proxy(redis_db=PROXY_DB, **PROXIES_CONFIG)
    p.server()
