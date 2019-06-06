# -*- coding:utf-8 -*-
import logging

import aiohttp

from setting.config import PROXY_DB
from utils.catch_utils import CatchUtils
from utils.redis_utils import RedisUtils
from utils.async_func_utils import async_func_pool

__author__ = 'zhoujifeng'
__date__ = '2019/6/5 19:22'

logger = logging.getLogger('comment')


class Comment(object):
    def __init__(self, async_func, proxy_db, redis_label='default'):
        self.proxy_cache = CatchUtils(RedisUtils.get_pool_by_label(redis_label, proxy_db))
        self.async_func_pool = async_func

    def server(self):
        while True:
            pass

    def get_proxy(self, ):
        ip = 'http://{}'.format(self.proxy_cache.randomkey())
        proxies = {
            'http': ip,
            'https': ip,
        }
        return proxies

    async def comment(self, url, city, ):
        async with aiohttp.ClientSession() as session:
            r = await self.get(session, 'https://www.baidu.com')
            return [id, r]

    async def get(self, session, *args, **kwargs):
        async with session.get(*args, **kwargs) as req:
            return await req.text()

    async def callback(x):
        print(x)

    async def except_callback(x):
        print(x)


if __name__ == '__main__':
    Comment(async_func_pool, PROXY_DB)
