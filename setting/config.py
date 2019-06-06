# -*- coding:utf-8 -*-
import os

import redis

from setting.setting import DATABASES, REDIS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_SOURCE = {
    'default': r'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=%(charset)s' %
               DATABASES['default'],
}

PROXIES_CONFIG = {
    # 3分钟代理包量
    # 'api': 'http://www.uu-ip.com/Tools/proxyIP.ashx?OrderNumber=89fd564c5f97be2ed3c4d6dd0af0384b&poolIndex=77091&cache=1&qty={}',
    # 包天代理
    'api_url': 'http://www.uu-ip.com/Tools/proxyIP.ashx?OrderNumber=89fd564c5f97be2ed3c4d6dd0af088b&poolIndex=75081&cache=1&Split=JSON2&qty={}',
    'pool_size': 2,  # 代理池大小
    'time_out': 3 * 60,  # 代理ip超时时间
    'batch': 200,  # 接口最大请求数量
    'redis_key': 'proxy_cache'  # redis中代理池的key
}
REDIS_CONN = {
    'default': lambda n: redis.Redis(
        connection_pool=redis.ConnectionPool(db=n, decode_responses=True, **REDIS['default'])),
}

ProcessesNum = 16

# redis设置
DEFAULT_REDIS_TIMEOUT = 60 * 60 * 24
CACHE_DB = 15  # redis数据缓存库
PROXY_DB = 0  # redis代理池数据库
