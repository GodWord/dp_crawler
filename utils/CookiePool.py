# -*- coding:utf-8 -*-
import random

from utils.Chromedp.chromedp import Chromedp

__author__ = 'zhoujifeng'
__date__ = '2019/4/4 14:17'


class CookieUtils:
    def __init__(self, pool_size=10):
        self.cookie_pool = dict()
        self.pool_size = pool_size

    def cookie(self, proxies):
        ch = Chromedp(proxies)
        ch.clear_browser_cookies()
        ch.clear_browser_cache()
        ch.open_url('https://www.dianping.com/chongqing/ch10')
        ch.wait_visible('/html/body/div[2]/div[3]/div[1]/div[1]')
        data = ch.get_cookies()
        cookie = ';'.join(str(value['name'] + ':' + value['value']) for value in data)
        return cookie

    def update(self, city, cookie, proxies):
        self.cookie_pool[city].remove(cookie)
        while True:
            cookie = self.cookie(proxies)
            if city in self.cookie_pool.keys():
                self.cookie_pool[city].append(cookie)
            else:
                self.cookie_pool[city].append([cookie])
            if len(self.cookie_pool[city]) >= self.pool_size:
                break

    def get(self, city):
        return random.choice(self.cookie_pool[city])
