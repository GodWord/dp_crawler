# -*- coding:utf-8 -*-

__author__ = 'zhoujifeng'
__date__ = '2019/4/4 14:57'

import redis

from setting.config import DEFAULT_REDIS_TIMEOUT as default_timeout


class CatchUtils:
    def __init__(self, redis_pool, prefix='dp_pydev_'):
        self.cache = redis.Redis(connection_pool=redis_pool)
        self.prefix = prefix

    def set(self, key, value, timeout=default_timeout):
        """
        保存缓存
        :param value:
        :param key:
        :param timeout:
        :return:
        """
        real_key = self.prefix + key
        self.cache.set(real_key, value)
        self.cache.expire(real_key, timeout)

    def lpush(self, key, value, timeout=default_timeout):
        """
        保存缓存
        :param value:
        :param key:
        :param timeout:
        :return:
        """
        real_key = self.prefix + key
        self.cache.lpush(real_key, *value)
        self.cache.expire(real_key, timeout)

    def mset(self, values: dict, timeout=default_timeout):
        """
        保存缓存
        :param timeout:
        :return:
        """

        self.cache.mset(values)
        list(map(lambda x: self.cache.expire(x, timeout), values.keys()))

    def hset(self, name, key, value, timeout=default_timeout):
        """
        保存缓存
        :param key:
        :param timeout:
        :return:
        """
        real_name = self.prefix + name
        self.cache.hset(real_name, key, value)
        self.cache.expire(real_name, timeout)

    def llen(self, key):
        """
        返返回存储在 key里的list的长度
        :param key:
        :return:
        """
        real_name = self.prefix + key
        return self.cache.llen(real_name)

    def hlen(self, name):
        """
        返回 key 指定的哈希集包含的字段的数量
        :param name:
        :return:
        """
        real_name = self.prefix + name
        return self.cache.hlen(real_name)

    def hmset(self, name, timeout=default_timeout, **kwargs):
        """
        保存缓存
        :param key:
        :param timeout:
        :return:
        """
        real_name = self.prefix + name
        self.cache.hmset(real_name, kwargs)
        self.cache.expire(real_name, timeout)

    def hget(self, name, key):
        """
        获取缓存的值
        :param key:
        :return:
        """
        real_name = self.prefix + name

        return self.cache.hget(real_name, key)

    def hgetall(self, name):
        """
        获取缓存的值
        :param name:
        :return:
        """
        real_name = self.prefix + name

        return self.cache.hgetall(real_name)

    def hmget(self, name, *args):
        """
        获取缓存的值
        :param name:
        :param args:
        :return:
        """
        real_name = self.prefix + name

        return self.cache.hmget(real_name, *args)

    def get(self, key):
        """
        获取缓存的值
        :param key:
        :return:
        """
        real_key = self.prefix + key
        return self.cache.get(real_key)

    def srem(self, key, member):
        """
        在key集合中移除指定的元素
        :param key:
        :param member:待移除元素一个或多个
        :return:从集合中移除元素的个数，不包括不存在的成员
        """
        self.cache.srem(key, member)

    def randomkey(self):
        return self.cache.randomkey()

    def delete(self, key):
        """
        清空缓存的值
        :param key:
        :return:
        """
        real_key = self.prefix + key
        return self.cache.delete(real_key)

    def dbsize(self):
        return self.cache.dbsize()

    def hexists(self, name, key):
        real_name = self.prefix + name

        return self.cache.hexists(real_name, key)
