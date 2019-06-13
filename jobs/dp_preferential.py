# -*- coding:utf-8 -*-
import pickle

import pandas as pd

from jobs.dp_comment.shop import Shop
from utils.db_utils import DBUtils

__author__ = 'zhoujifeng'
__date__ = '2019/3/25 14:15'

from logging.config import dictConfig

from setting.config import PreferentialRedis
from utils.catch_utils import CatchUtils
from utils.logger import LOGGING
from utils.redis_utils import RedisUtils

import logging
import random
import time
import aiohttp

from models.preferential import Preferential
from utils.CrawlerUtils import CrawlerUtils
from utils.DPUtils import DPUtils
from utils.NewDynamicModel import NewDynamicModel
from utils.NewDynamicModel import NewDynamicModel as ndw
from utils.requests_utils import RequestsUtils

logger = logging.getLogger('DPPreferential')


class DPPreferential:

    def __init__(self, redis_db, redis_label='default'):
        self.url = 'https://m.dianping.com/shop/{}'
        self.req = RequestsUtils()
        self.history_cache = CatchUtils(RedisUtils.get_pool_by_label(redis_label, redis_db))
        self.exists_key = 'preferential'
        self.exists_time_out = 60 * 60 * 24 * 365

    def run(self):
        df_shop = self.get_shop()

        def __deal(shop):
            if not self.history_cache.hexists(self.exists_key, shop['shop_id']):
                self.get_preferential(shop['shop_id'], shop['city'])

        df_shop.apply(__deal, axis=1)

    def get_preferential(self, shop_id, city):
        url = self.url.format(shop_id)
        self.req.set_cookies(city)
        content = self.req.get(url, callback=lambda x: x.text, referer='m.dianping.com')
        content = CrawlerUtils.get_bs(content, '.shop-tuan-list .cnt .content')
        if not content:
            logger.info('商家[%d]没有优惠信息' % (shop_id,))
            logger.info('开始休眠')
            return

        data = list(map(lambda x: {
            'shop_id': shop_id,
            'name': x.select('.newtitle')[0].text.strip(),
            'sold': x.select('.soldNumNew')[0].text.strip()[2:],
            'price': x.select('.price')[0].text.strip(),
            'old_price': x.select('.o-price')[0].text.strip(),
            'uuid': CrawlerUtils.get_md5_value(str(shop_id) + x.select('.newtitle')[0].text.strip()),
        }, content))
        uuid_list = list(map(lambda x: x['uuid'], data))
        exists_preferential_uuid = self.get_exists_preferential(uuid_list)
        update_data = list()
        insert_data = list()
        list(map(lambda x: update_data.append(x) if x['uuid'] in exists_preferential_uuid else insert_data.append(x),
                 data))

        if update_data.__len__() > 0:
            NewDynamicModel.update(Preferential, update_data, 'uuid')
        if insert_data.__len__() > 0:
            NewDynamicModel.save_to_db(Preferential, insert_data)

        self.history_cache.hset(self.exists_key, shop_id, pickle.dumps(uuid_list), self.exists_time_out)

    @staticmethod
    def get_exists_preferential(uuid_list):
        session = DBUtils.get_session_by_model(Preferential)

        exists_preferential = list(
            map(lambda x: x.uuid, session.query(Preferential.uuid).filter(Preferential.uuid.in_(uuid_list)).all()))
        session.close()
        return exists_preferential

    def get_shop(self):
        shop_data = ndw.get_data_by_model(Shop, lambda x, y: x.query(y.shop_id, y.city)
                                          .filter(y.is_expire == 0)
                                          # .filter(y.stars >= 35)
                                          .all())
        df = pd.DataFrame(shop_data)
        return df


if __name__ == '__main__':
    dictConfig(LOGGING)

    pre = DPPreferential(PreferentialRedis)
    pre.run()
