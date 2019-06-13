# -*- coding:utf-8 -*-
__author__ = 'zhoujifeng'
__date__ = '2018/10/16 10:53'
import hashlib
import re
from datetime import datetime

import pandas as pd
import pymysql
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, mapper

from setting.setting import DATABASES


class DBUtils(object):
    _tmp_cls_dit = dict()
    _session = dict()
    _engine_dict = dict()

    @classmethod
    def get_tb_name(cls, tb_name, start_time=None, end_time=None, hours=None, days=None, months=None, **kwargs):
        """
        获取表名
        :param tb_name: 表名
        :param time_interval: 分表时间间隔(小时)
        :param start_time: 需要查询的开始时间(当end_time小于等于start_time时返回start_time对应表名)
        :param end_time: 需要查询的结束时间(没有则返回start_time所对应名称)
        :return: list查询时间对应的表名列表,
                name_2018_08_24_1_11
                name          表名
                2018_08_24    当前日期
                1             数据库建表间隔时间(小时)
                11            用于区别当日的表(值越大时间越偏后)
        example:
            start_time = datetime.strptime("2018-09-08 01:34:52", "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime("2018-09-10 01:34:42", "%Y-%m-%d %H:%M:%S")
            for i in get_tb_name_by_model('test', 4, start_time, end_time):
                print(i)
            >>> print
                test_2018_09_09_4_0
                test_2018_09_09_4_1
                test_2018_09_09_4_2
                test_2018_09_09_4_3
                test_2018_09_09_4_4
                test_2018_09_09_4_5
                test_2018_09_10_4_0
        """

        if not isinstance(start_time, datetime):  # 判断start_time是否为datetime的实例
            raise TypeError('{0} is not datetime instance'.format(start_time, ))

        if end_time is not None and not isinstance(end_time, datetime):  # 判断end_time是否为datetime的实例
            raise TypeError('{0} is not datetime instance'.format(end_time, ))
        if hours is not None:
            time_interval = hours
            time_interval_tpye = 'hour'
        elif days is not None:
            time_interval = days
            time_interval_tpye = 'day'

        elif months is not None:
            time_interval = months
            time_interval_tpye = 'month'
        else:
            raise TypeError('{0}()参数错误'.format(DBUtils.get_tb_name.__name__))

        def __get_name(tb_name, start_time):
            result_name = ''
            if hours is not None and days is None and months is None:
                time_interval = hours

                start_date = start_time.strftime('%Y_%m_%d')
                db_num = start_time.hour // time_interval
                result_name = tb_name + '_' + start_date + '_' + str(time_interval) + '_' + str(db_num)
            elif days is not None and hours is None and months is None:
                time_interval = days
                start_date = start_time.strftime('%Y_%m_%d')
                if time_interval == 1:
                    result_name = tb_name + '_' + start_date
                else:

                    end_date = (start_time + relativedelta(days=time_interval - 1)).strftime('%Y_%m_%d')
                    result_name = tb_name + '_' + start_date + '__' + end_date
            elif months is not None and hours is None and days is None:
                time_interval = months
                start_date = start_time.strftime('%Y_%m')

                if time_interval == 1:

                    result_name = tb_name + '_' + start_date

                else:
                    end_date = (start_time + relativedelta(months=1)).strftime('%Y_%m')

                    result_name = tb_name + '_' + start_date + '___' + end_date
            else:
                raise TypeError('{0}参数错误'.format(__get_name.__name__))
            return result_name

        tb_name_lower = DBUtils.get_tb_name_lower(tb_name=tb_name)
        date = start_time
        if end_time is None:  # 若end_time不存在则只返回start_time所对应名称
            yield __get_name(tb_name_lower, start_time)
        elif end_time <= start_time:  # 若end_time小于start_time则返回start_time所对应名称
            yield __get_name(tb_name_lower, start_time)
        else:
            diff_time = relativedelta(microseconds=0)
            if time_interval_tpye == 'day':
                day = start_time.day // time_interval * time_interval  # 获取start_time所对应的起始时间
                date = start_time.replace(hour=0, minute=0, second=0)  # 获取起始时间(datetime)

                diff_time = relativedelta(days=time_interval)
            elif time_interval_tpye == 'hour':
                hour = start_time.hour // time_interval * time_interval  # 获取start_time所对应的起始时间
                date = start_time.replace(hour=hour, second=0, minute=0)  # 获取起始时间(datetime)

                diff_time = relativedelta(hours=time_interval)
            elif time_interval_tpye == 'month':

                date = start_time.replace(day=1, hour=0, second=0, minute=0)  # 获取起始时间(datetime)

                diff_time = relativedelta(months=time_interval)

            while True:
                yield __get_name(tb_name_lower, date)  # 返回名称
                date = date + diff_time  # 上次返回时间加上分表间隔时长
                if end_time <= date:  # 退出循环
                    break

    @classmethod
    def get_tb_name_lower(cls, tb_name):
        """
        将model名称由驼峰命名转换为小写带下划线的名称
        :param tb_name: 表名
        :return: type:str 转换后的表名
        """
        for s in tb_name:  # type: str
            if ord(s) in range(65, 91):
                tb_name = tb_name.replace(s, '_' + s.lower())  # type:str
        if tb_name.startswith('_'):
            tb_name = tb_name[1:]
        return tb_name

    @classmethod
    def table_exists(cls, cur, table_name):
        """"
        判断表是否存在
        :param cur: 数据库游标
        :param table_name: 需要判断的表名
        :return: 存在返回True,不存在返回False
        """
        sql = "show tables;"
        cur.execute(sql)
        tables = [cur.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]

        if table_name in table_list:
            return True  # 存在返回True
        else:
            return False  # 不存返回False

    @classmethod
    def get_datetime(cls, str_time):
        return datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_suffix(cls, model_cls, table_name: str):
        """
        根据基础类型和表名 获取表后缀
        :param model_cls:
        :param table_name:
        :return:
        """
        table_prefix = cls.get_tb_name_lower(model_cls.__name__)
        table_suffix = table_name.replace(table_prefix, '', 1)
        return table_suffix[1:]

    @classmethod
    def get_suffix_by_models(cls, base_cls, start_time):
        """
        根据模型类型生成后缀
        :param base_cls:
        :param start_time:
        :return:
        """
        ext = {
            'hours': 4
        }
        if hasattr(base_cls, 'ext'):
            ext = dict(
                (name, getattr(base_cls.ext(), name)) for name in dir(base_cls.ext()) if not name.startswith('__'))

        return next(DBUtils.get_tb_name('', start_time, start_time, **ext))[1:]

    @classmethod
    def get_suffix_by_timestamp(cls, base_cls, time_stamp):
        """
        根据时间戳获取后缀
        :param base_cls:
        :param time_stamp:
        :return:
        """
        start_time = datetime.strptime(str(time_stamp), "%Y-%m-%d %H:%M:%S")
        return DBUtils.get_suffix_by_models(base_cls, start_time)

    @classmethod
    def get_md5_value(cls, value):
        # 将字符串转成md5
        md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
        md5.update(value.encode("utf8"))  # 得到MD5消息摘要
        md5_vlaue = md5.hexdigest()  # 以16进制返回消息摘要，32位
        return md5_vlaue

    @classmethod
    def get_session_by_model(cls, base_cls):
        """
        通过model获取session
        :param base_cls:
        :return:
        """
        app_label = getattr(getattr(base_cls, 'info', None), 'app_label', 'default')
        if app_label not in cls._session.keys():
            SessionCls = sessionmaker(bind=DBUtils.get_engine_by_label(app_label))
            New_SessionCls = scoped_session(SessionCls)
            session = New_SessionCls()

            cls._session[app_label] = session
        return cls._session[app_label]

    @classmethod
    def get_dataframe(cls, base_cls, objs):
        cols = DBUtils.get_fields(base_cls)
        if len(objs) == 0:
            return
        if isinstance(objs[0], base_cls):
            data_list = list(map(lambda ob: list(getattr(ob, column_name, None) for column_name in cols), objs))
            df = pd.DataFrame(data_list, columns=cols)
            drop_list = list()
            if 'info' in cols:
                drop_list.append('info')
            if 'ext' in cols:
                drop_list.append('ext')
            df.drop(drop_list, axis=1, inplace=True)
        else:
            df = pd.DataFrame(objs)
        return df

    @classmethod
    def get_fields(cls, base_cls):
        return list(name for name in dir(base_cls) if not name.startswith('__'))

    @classmethod
    def get_table_name_by_timestamp(cls, base_cls, time_stamp=None):
        """
        通过时间戳和类来获取表名
        :param base_cls:
        :param time_stamp:
        :return:
        """

        if not hasattr(base_cls, 'ext'):
            return 'da_' + base_cls.__name__.lower()
        else:
            ext = dict(
                (name, getattr(base_cls.ext(), name)) for name in dir(base_cls.ext()) if not name.startswith('__'))
            start_time = datetime.strptime(str(time_stamp).split('.')[0], "%Y-%m-%d %H:%M:%S")
            return next(DBUtils.get_tb_name(base_cls.__name__, start_time, start_time, **ext))

    @classmethod
    def get_oracle_table_name_by_datetime(cls, table_name: str, date_time: datetime):
        return table_name + date_time.strftime('%Y%m')

    @classmethod
    def get_table_name_by_ymd(cls, base_cls, ymd):
        """根据ymd获取表名"""
        if not hasattr(base_cls, 'ext'):
            return 'da_' + base_cls.__name__.lower()
        else:
            ext = dict(
                (name, getattr(base_cls.ext(), name)) for name in dir(base_cls.ext()) if not name.startswith('__'))
            start_time = datetime.strptime(str(ymd), "%Y%m%d")
            return next(DBUtils.get_tb_name(base_cls.__name__, start_time, start_time, **ext))

    @classmethod
    def db_source(cls, name):
        if name not in DATABASES.keys():
            raise Exception('配置项中未找到该数据库')
        return 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=%(charset)s;' % (DATABASES[name])

    @classmethod
    def get_conn_by_model(cls, model_cls=None, app_label='default'):
        if model_cls and hasattr(model_cls, 'info') and hasattr(getattr(model_cls, 'info'), 'app_label'):
            app_label = getattr(getattr(model_cls, 'info'), 'app_label')

        return pymysql.connect(**DATABASES[app_label])

    @classmethod
    def get_engine_by_label(cls, label):
        if label not in DATABASES.keys():
            raise KeyError('配置项中未找到该数据库')
        if label not in cls._engine_dict.keys():
            database_uri = 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s?charset=utf8' % \
                           (DATABASES[label])
            engine = create_engine(database_uri, pool_size=500, pool_recycle=3600, echo=False, max_overflow=-1,
                                   pool_pre_ping=True, )
            cls._engine_dict[label] = engine
        return cls._engine_dict[label]
