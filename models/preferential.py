# -*- coding:utf-8 -*-
__author__ = 'zhoujifeng'
__date__ = '2019/3/25 16:13'

from datetime import datetime

from sqlalchemy import BigInteger, Column, Integer, String, DateTime, create_engine, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from setting.config import DB_SOURCE

Base = declarative_base()

engine = create_engine(DB_SOURCE['default'], encoding="utf-8", echo=False)


class Preferential(Base):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    __tablename__ = "preferential"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(BigInteger, nullable=True, index=True, comment='商家ID')
    name = Column(String(255), nullable=True, default=0, comment='优惠名称')
    sold = Column(Integer, nullable=True, default=0, comment='已售数量')
    price = Column(Integer, nullable=True, comment='商品价格')
    old_price = Column(Integer, nullable=True, comment='商品原价')
    uuid = Column(String(32), nullable=True, comment='唯一标识(基于商家ID与优惠名称)')

    int1 = Column(Integer, nullable=True, comment='备用字段')
    int2 = Column(Integer, nullable=True, comment='备用字段')
    int3 = Column(Integer, nullable=True, comment='备用字段')
    str1 = Column(String(800), nullable=True, comment='备用字段')
    str2 = Column(String(800), nullable=True, comment='备用字段')
    str3 = Column(String(800), nullable=True, comment='备用字段')
    float1 = Column(Float, nullable=True, comment='备用字段')
    float2 = Column(Float, nullable=True, comment='备用字段')
    float3 = Column(Float, nullable=True, comment='备用字段')
    bool1 = Column(Boolean, nullable=True, comment='备用字段')
    bool2 = Column(Boolean, nullable=True, comment='备用字段')
    bool3 = Column(Boolean, nullable=True, comment='备用字段')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


Base.metadata.create_all(engine)  # 创建表结构
