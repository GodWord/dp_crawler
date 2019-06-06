# -*- coding:utf-8 -*-
import json
import logging
import random
from http import client
from json import JSONDecodeError

from utils.ProxiesPool import ProxiesPool

__author__ = 'zhoujifeng'
__date__ = '2019/3/12 21:06'

import requests

logger = logging.getLogger('dp_shop')


class RequestsUtils:
    def __init__(self, proxies_config, cookies_list=None, ):
        self.cookies_list = cookies_list or list()
        self.proxies_pool = ProxiesPool(proxies_config)
        self.last_proxies = dict()

        self.session = requests.Session()
        self.session.keep_alive = False  # 关闭多余连接
        self.req = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Cookie": "cy=9; cye=chongqing; _lxsdk_cuid=16990dc041dc8-03950f45647727-7a1b34-2a3000-16990dc041dc8; _lxsdk=16990dc041dc8-03950f45647727-7a1b34-2a3000-16990dc041dc8; _hc.v=5b583263-7c12-0e9a-9ed1-ade1854ff183.1552913532; lgtoken=06fa50c8e-368e-46bf-bc93-d70de929d862; s_ViewType=10; _lxsdk_s=16990dc041d-8cc-f09-f07%7C%7C82",
            "Proxy-Connection": "close",
            'Connection': 'close',
        }

    def get(self, url, referer=None, params=None, stream=False, timeout=2, **kwargs):
        self.headers['Cookie'] = random.choice(self.cookies_list)
        if referer:
            self.headers['Referer'] = referer
        logger.info('正在请求:[%s]' % (url,))
        self.last_proxies = self.proxies_pool.proxies()
        try:
            self.req = self.session.get(url, headers=self.headers, proxies=self.last_proxies,
                                        params=params, stream=stream, timeout=timeout, **kwargs)
            self.req.raise_for_status()
            self.req.encoding = 'utf-8'
        except AttributeError as e:
            logger.error('req:[%s]:' % (self.req,))
            raise e
        except Exception as e:
            raise e

    def post(self, url, referer=None, headers=None, json_data=None, stream=False, timeout=5, **kwargs):
        if not headers:
            headers = self.headers
        headers['Cookie'] = random.choice(self.cookies_list)
        if referer:
            self.headers['Referer'] = referer
        logger.info('正在请求:[%s],json:%s' % (url, json_data))
        self.last_proxies = self.proxies_pool.proxies()

        try:
            self.req = self.session.post(url, headers=headers, json=json_data, proxies=self.last_proxies,
                                         stream=stream, timeout=timeout, **kwargs)
            self.req.raise_for_status()
        except Exception as e:
            # self.proxies_pool.update(proxies)
            raise e

    def text(self):
        return self.req.text

    def content(self):
        return self.req.content

    def json(self):
        try:
            return self.req.json()
        except JSONDecodeError as e:
            logger.error(e)
            raise e

    def close(self):
        self.req.close()
