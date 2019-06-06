# -*- coding:utf-8 -*-
import logging

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from apps.dp_shop.models.cookie import Cookie
from setting.config import DB_SOURCE
from utils.DBUtils import DBUtils

logger = logging.getLogger('NewDynamicModel')

Model_Base = declarative_base()


class NewDynamicModel:
    _instance = dict()

    def __new__(cls, base_cls, tb_name, is_tmp=False):
        """
        根据名称生成model类型
        :param base_cls:
        :param tb_name:
        :return:
        """
        new_cls_name = "%s_To_%s" % (base_cls.__name__, '_'.join(map(lambda x: x.capitalize(), tb_name.split('_'))))
        # 获取配置的链接
        if new_cls_name not in cls._instance:
            Model_Base.metadata.clear()
            model_cls = type(tb_name, (base_cls, Model_Base,), {'__tablename__': tb_name})
            # 创建表
            app_label = getattr(getattr(base_cls, 'info', None), 'app_label', 'default')
            Model_Base.metadata.create_all(DBUtils.get_engine_by_label(app_label))
            if is_tmp:
                return model_cls
            cls._instance[new_cls_name] = model_cls

        return cls._instance[new_cls_name]

    @staticmethod
    def get_session():
        """
        获取数据库session
        :return:db_session
        """
        # 根据setting配置获取session
        SessionCls = sessionmaker(
            bind=create_engine(DB_SOURCE['default'], pool_size=1000, pool_recycle=3600, echo=False, max_overflow=-1))
        New_SessionCls = scoped_session(SessionCls)
        session = New_SessionCls()

        return session

    @classmethod
    def stage_by_cls(cls, base_cls, df: pd.DataFrame, batch=500):
        """
        TODO:需要测试
        批量保存数据
        :param base_cls:
        :param df:
        :return:
        """

        def __deal(table_name, tmp_data: pd.DataFrame):
            tmp_df = tmp_data.copy()
            new_cls = NewDynamicModel(base_cls, table_name)
            tmp_df.drop(['table_name'], axis=1, inplace=True)
            session = DBUtils.get_session_by_model(new_cls)

            def __inner_create(i):
                # 进行批量保存
                datas = cls.build_to_model_by_dataFrame(new_cls, tmp_df.iloc[i:i + batch, :])
                try:
                    session.bulk_save_objects(datas)
                    session.commit()
                except Exception as e:
                    logger.error('[%s]数据保存出错,数据共:[%d]条' % (new_cls.__name__, len(datas)))
                    logger.error(e)
                    raise e

            list(map(__inner_create, range(0, tmp_df.__len__(), batch)))
            session.close()

        list(map(lambda x: __deal(*x), df.groupby(by='table_name')))
        logger.info('[%s]保存完成' % (base_cls.__name__,))

    @staticmethod
    def save_to_db(model, data, db_session=None):
        try:
            logger.info(data)
            # 获取session
            if not db_session:
                db_session = NewDynamicModel.get_session()
            # 在session中添加数据

            db_session.bulk_save_objects(map(lambda x: model(**x), data))
            # commit(这里不提交数据库是不会保存的)
            db_session.commit()
        except Exception as e:
            logger.error(e)
            logger.error(data)

    @staticmethod
    def update(model, data, field='id'):
        logger.info('开始更新数据')
        session = NewDynamicModel.get_session()
        if hasattr(model, field):
            list(map(lambda x: session.query(model).filter(getattr(model, field) == x[field]).update(x), data))
            session.commit()
            logger.info('数据更新完成')
        else:
            raise Exception('[%s]没有[%s]属性值' % (model.__name__, field))

    @classmethod
    def get_cookies(cls, city, cookie_type=0):
        session = cls.get_session()
        data = session.query(Cookie.cookie).filter_by(city=city, type=cookie_type).all()

        return list(map(lambda x: x[0], data))

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
    def get_data_by_model(cls, base_cls, fn, session):
        # db_session = NewDynamicModel.get_session()
        data = fn(session, base_cls)
        return data

    @classmethod
    def build_to_model_by_dataFrame(cls, base_cls, df: pd.DataFrame):
        def inner(data):
            data = data[1]  # type: pd.Series
            tmp_data = data.to_dict()  # type:dict
            # 把id字段交给 外部控制
            # if 'id' in tmp_data.keys():
            #     del tmp_data['id']
            return base_cls(**tmp_data)

        datas = list(map(inner, df.T.iteritems()))
        return datas

    # @classmethod
    # def get_cookies(cls, url, xpath, proxies_pool=None, __pool_size=5, is_pc=True):
    #     cookie_pool = list()
    #     logger.info('开始获取cookie,共需获取[%d]个cookie,URL:[%s]' % (__pool_size, url))
    #     error_count = 0
    #     while True:
    #
    #         proxy = random.choice(proxies_pool)
    #         logger.info('proxy:%s' % (proxy,))
    #         ch = Chromedp(is_pc=is_pc, proxy=proxy)
    #         try:
    #             ch.clear_browser_cookies()
    #             ch.clear_browser_cache()
    #             ch.open_url(url)
    #             ch.wait_visible(xpath)
    #             data = ch.get_cookies()
    #             ch.quit()
    #             cookie = ';'.join(str(value['name'] + ':' + value['value']) for value in data)
    #             cookie_pool.append(cookie)
    #             logger.info('已获取[%d]个cookie，当前获取:[%s]' % (len(cookie_pool), cookie,))
    #         except Exception as e:
    #             ch.quit()
    #             logger.error(e)
    #
    #             error_count += 1
    #             if error_count > 5:
    #                 logger.error('错误连续超过5次，退出循环')
    #                 raise e
    #             continue
    #         error_count = 0
    #         if len(cookie_pool) >= __pool_size:
    #             logger.info('获取完成，')
    #             break
    #         time.sleep(random.randint(3, 5))
    #     return cookie_pool
    # @classmethod
    # def get_db_pool(cls):
    #     """
    #     获取数据库连接池
    #     :return:
    #     """
    #     db_pool = PooledDB(
    #         creator=pymysql,  # 使用链接数据库的模块
    #         maxconnections=8,  # 连接池允许的最大连接数，0和None表示没有限制
    #         mincached=5,  # 初始化时，连接池至少创建的空闲的连接，0表示不创建
    #         maxcached=8,  # 连接池空闲的最多连接数，0和None表示没有限制
    #         # 连接池中最多共享的连接数量，0和None表示全部共享，ps:其实并没有什么用，因为pymsql和MySQLDB等模块中的threadsafety都为1，所有值无论设置多少，_maxcahed永远为0，所以永远是所有链接共享
    #         maxshared=3,
    #         blocking=True,  # 链接池中如果没有可用共享连接后，是否阻塞等待，True表示等待，False表示不等待然后报错     setsession = [],#开始会话前执行的命令列表
    #         ping=0,  # ping Mysql 服务端，检查服务是否可用
    #         charset='utf8',
    #         **DATABASES['default']
    #     )
    #     return db_pool
