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

logger = logging.getLogger('http')


class RequestsUtils:
    def __init__(self, proxies_config, cookies_list=None, ):
        self.cookies_list = cookies_list or list()
        self.proxies_pool = ProxiesPool(proxies_config)
        self.last_proxies = dict()

        self.session = requests.Session()
        self.session.keep_alive = False  # 关闭多余连接
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Cookie": "cy=9; cye=chongqing; _lxsdk_cuid=16990dc041dc8-03950f45647727-7a1b34-2a3000-16990dc041dc8; _lxsdk=16990dc041dc8-03950f45647727-7a1b34-2a3000-16990dc041dc8; _hc.v=5b583263-7c12-0e9a-9ed1-ade1854ff183.1552913532; lgtoken=06fa50c8e-368e-46bf-bc93-d70de929d862; s_ViewType=10; _lxsdk_s=16990dc041d-8cc-f09-f07%7C%7C82",
            "Proxy-Connection": "close",
            'Connection': 'close',
        }

    def get(self, url, callback=None, referer=None, params=None, stream=False, is_pc=False, timeout=2, **kwargs):
        self.headers['Cookie'] = random.choice(self.cookies_list)
        if referer:
            self.headers['Referer'] = referer
        logger.info('正在请求:[%s]' % (url,))
        self.headers['User-Agent'] = self.get_headers(is_pc)
        self.last_proxies = self.proxies_pool.proxies()
        try:
            req = self.session.get(url, headers=self.headers, proxies=self.last_proxies,
                                   params=params, stream=stream, timeout=timeout, **kwargs)
            req.raise_for_status()
            req.encoding = 'utf-8'
            if not callback:
                res = callback(req)
                req.close()
                return res

        except Exception as e:
            raise e

    def post(self, url, callback=None, referer=None, json_data=None, stream=False, is_pc=False, timeout=5,
             **kwargs):
        self.headers['Cookie'] = random.choice(self.cookies_list)
        self.headers['User-Agent'] = self.get_headers(is_pc)

        if referer:
            self.headers['Referer'] = referer
        logger.info('正在请求:[%s],json:%s' % (url, json_data))
        self.last_proxies = self.proxies_pool.proxies()

        try:
            req = self.session.post(url, headers=self.headers, json=json_data, proxies=self.last_proxies,
                                    stream=stream, timeout=timeout, **kwargs)
            req.raise_for_status()
            if callback is not None:
                res = callback(req)
                req.close()
                return res

        except Exception as e:
            # self.proxies_pool.update(proxies)
            raise e

    @classmethod
    def get_headers(cls, is_pc=False):
        pc_headers = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.1.6000',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) WkshBrowser/49.0.2623.110 Safari/537.36',

        ]
        mobile_headers = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12. Mobile/16D57 Safari/600.1.4 baidubrowser/4.14.1.11 (Baidu; P2 12.1.4)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/16D57 UCBrowser/12.3.0.1138 Mobile AliApp(TUnionSDK/0.1.20.3)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 MQQBrowser/9.0.3 Mobile/16D57 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X; zh-cn) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/16D57 Quark/3.0.6.926 Mobile',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) OPiOS/12.0.5.3 Version/7.0 Mobile/16D57 Safari/9537.53',
            'Mozilla/5.0 (Linux; Android 7.0; SLA-AL00 Build/HUAWEISLA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36 MicroMessenger/6.6.3.1260(0x26060339) NetType/4G Language/zh_CN',
            'Mozilla/5.0 (Linux; Android 7.0; SLA-AL00 Build/HUAWEISLA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.3.1260(0x26060339) NetType/4G Language/zh_CN'
            'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
        ]
        if is_pc:
            return random.choice(pc_headers)
        else:
            return random.choice(mobile_headers)
