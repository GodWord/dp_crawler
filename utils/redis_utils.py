# -*- coding:utf-8 -*-
import redis

from setting.setting import REDIS

__author__ = 'zhoujifeng'
__date__ = '2019/6/5 21:16'


class RedisUtils:
    # redis连接池
    __redis_pools = dict()

    @classmethod
    def get_pool_by_label(cls, label, db):
        key = '{}_{}'.format(label, db)

        if key not in cls.__redis_pools.keys():
            pool = redis.ConnectionPool(db=db, decode_responses=True, **REDIS[label])
            cls.__redis_pools[key] = pool

        return cls.__redis_pools[key]
