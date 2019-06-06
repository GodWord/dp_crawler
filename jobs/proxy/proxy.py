# -*- coding:utf-8 -*-
import time

from setting.config import PROXIES_CONFIG, PROXY_DB

__author__ = 'zhoujifeng'
__date__ = '2019/6/5 19:59'

import logging
from logging.config import dictConfig

import requests

from utils.logger import LOGGING
from utils.catch_utils import CatchUtils
from utils.redis_utils import RedisUtils

logger = logging.getLogger('proxy')


class Proxy:
    def __init__(self, api_url, pool_size, time_out, redis_key, redis_db, batch=200, redis_label='default'):
        logger.info('[Proxy]开始初始化')
        self.__api_url = api_url
        self.__pool_size = pool_size
        self.__time_out = time_out
        self.__proxy_key = redis_key
        self.__batch = batch
        self.__session = requests.Session()
        self.__init_session__()

        self.catch = CatchUtils(RedisUtils.get_pool_by_label(redis_label, redis_db))

    def server(self):
        while True:
            size = self.catch.llen(self.__proxy_key)
            logger.info('当前代理池长度为:%d' % (size,))

            if size >= self.__pool_size:
                logger.info('代理池不需要更新,休眠1秒')
                time.sleep(1)
                continue
            diff_size = self.__pool_size - size
            while diff_size > 0:
                if diff_size < self.__batch:
                    length = diff_size
                else:
                    length = 200

                data = self.get(length)
                if data:
                    self.lpush(data)
                    diff_size -= 200

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
            return req.json()

        except Exception as e:
            logger.error(e)
            return None

    def hmset(self, data):
        """
        向redis中添加代理ip
        :param data:
        :return:
        """
        proxies_list = list(map(lambda x: '%(Ip)s:%(Port)s' % x, data['Data']))
        self.catch.lpush(self.__proxy_key, proxies_list, self.__time_out)

    def delete(self, proxy):
        """
        删除指定代理
        :param proxy: 待删除代理，一个或多个
        :return: 从集合中移除元素的个数，不包括不存在的成员
        """
        return self.catch.srem(self.__proxy_key, proxy)


if __name__ == '__main__':
    dictConfig(LOGGING)
    p = Proxy(redis_db=PROXY_DB, **PROXIES_CONFIG)
    p.server()
