# -*- coding:utf-8 -*-
import aiohttp

__author__ = 'zhoujifeng'
__date__ = '2019/6/7 10:27'


class AiohttpUtils:
    def __init__(self):
        pass

    def post(self, url, data, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(resp.cookies)
