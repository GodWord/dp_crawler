# -*- coding:utf-8 -*-
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
    def __init__(self, proxies_config):
        self.proxies_config = proxies_config
        self.pool_size = proxies_config['__pool_size']
        self.pool = list()
        self.__get_proxies()

    def get_content(self, url, depth=1):

        try:
            req = requests.get(url, headers=headers)
            req.raise_for_status()
            req.encoding = 'utf-8'
            content = req.text
            req.close()
            return content
        except Exception as e:
            if depth >= 5:
                raise e
            depth += 1
            time.sleep(3)
            self.get_content(url, depth)

    def __get_proxies(self, size=None, *args, **kwargs):

        try:
            url = self.proxies_config['api'].format(size or self.pool_size)
            html = self.get_content(url)

            data = html.strip().split('\r\n')
            logger.info('已获取代理:%s' % (data,))
            self.pool += list(map(lambda x: {
                "http": 'http://' + x,
                "https": 'http://' + x,
            }, data))
        except Exception:
            self.__get_proxies(size)

    def remove(self, data):
        logger.info('删除代理:[%s]' % (data,))
        if data in self.pool:
            self.pool.remove(data)

    def update(self, data):
        self.remove(data)
        while True:
            proxy = self.__get_proxies(size=1)
            if proxy is not None:
                self.pool += proxy
            if len(self.pool) >= self.pool_size:
                break
        logger.info('当前代理池大小:[%d]' % (len(self.pool, )))

    def proxies(self):
        proxy = random.choice(self.pool)
        return proxy
