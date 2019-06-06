# -*- coding:utf-8 -*-
__author__ = 'zhoujifeng'
__date__ = '2019/3/24 9:22'

import json
import os

from setting.config import BASE_DIR


class FileUtils:
    @classmethod
    def read_json_by_path(cls, path):
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as r:
            city = json.loads(r.read())
        return city

    @classmethod
    def get_comment_history_by_city(cls, path, city):
        """
        根据地区读取历史记录文件
        :param path:
        :param city:
        :return:
        """
        if not os.path.exists(path):
            os.mkdir(path)
        comment_path = os.path.join(path, 'comment_%s.json' % (city,))
        if not os.path.exists(comment_path):
            data = {"comment_type": 2, "offset": 0, "last_shop": 0, "exist_shop_id": []}
            with open(comment_path, 'w', encoding='utf-8') as w:
                w.write(json.dumps(data))
            return data
        with open(comment_path, 'r', encoding='utf-8') as r:
            res = cls.read_json_by_path(comment_path)
        return res

    @classmethod
    def save_comment_history_by_city(cls, path, city, cache_data):
        """
        根据地区读取历史记录文件
        :param path:
        :param city:
        :return:
        """
        comment_path = os.path.join(path, 'comment_%s.json' % (city,))
        with open(comment_path, 'w', encoding='utf-8') as w:
            w.write(json.dumps(cache_data))

    @classmethod
    def get_city(cls):
        path = os.path.join(BASE_DIR, 'static/json/city.json')
        data = cls.read_json_by_path(path)
        return data

    @staticmethod
    def update_city(last_page, last_city):
        path = os.path.join(BASE_DIR, 'static/json/city.json')
        with open(path, 'r+', encoding='utf-8') as r:
            city = json.loads(r.read())
        city['last_page'] = last_page
        city['last_city'] = last_city
        with open(path, 'w', encoding='utf-8') as w:
            w.write(json.dumps(city))

    @classmethod
    def save_json_by_path(cls, path, data):
        with open(path, 'w', encoding='utf-8') as w:
            w.write(json.dumps(data))


if __name__ == '__main__':
    FileUtils.update_city(10, '重庆')
