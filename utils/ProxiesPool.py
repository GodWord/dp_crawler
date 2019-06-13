# -*- coding:utf-8 -*-
from utils.catch_utils import CatchUtils
from utils.redis_utils import RedisUtils

__author__ = 'zhoujifeng'
__date__ = '2019/4/2 21:36'
import logging
import random
import time

import requests
from requests.exceptions import ChunkedEncodingError

logger = logging.getLogger('ProxiesPool')
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
    'Connection': 'close',
}


class ProxiesPool:
    def __init__(self, redis_db, redis_label='default', **kwargs):
        self.proxy_cache = CatchUtils(RedisUtils.get_pool_by_label(redis_label, redis_db))

    def proxies(self):
        ip = 'http://{}'.format(self.proxy_cache.randomkey())
        proxies = {
            'http': ip,
            'https': ip,
        }
        return proxies

    def update(self, proxies):
        try:
            ip = proxies['http'].split('//')[1]
            self.proxy_cache.delete(ip)
        except Exception as e:
            logger.error(e)
            logger.error('代理删除失败')
