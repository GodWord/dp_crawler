# -*- coding:utf-8 -*-
from datetime import datetime

from sqlalchemy import BigInteger, Column, Integer, String, DateTime, create_engine, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from setting.config import DB_SOURCE

Base = declarative_base()

engine = create_engine(DB_SOURCE['default'], encoding="utf-8", echo=False)


class Shop(Base):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    __tablename__ = "dp_shop"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(BigInteger, nullable=True, index=True, comment='商家ID')
    shop_name = Column(String(255), nullable=True, comment='商家名称')
    category_name = Column(String(64), nullable=True, comment='商家类别')
    avg_price = Column(Float, nullable=True, default=0, index=True, comment='人均价格')
    review_count = Column(Integer, nullable=True, default=0, comment='评论总数')
    stars = Column(Integer, nullable=True, index=True, comment='店铺评分')
    taste = Column(Float, nullable=True, index=True, comment='口味评分')
    surroundings = Column(Float, nullable=True, index=True, comment='环境评分')
    serve = Column(Float, nullable=True, index=True, comment='服务评分')
    city_name = Column(String(64), nullable=True, comment='城市名称')
    city = Column(String(64), nullable=True, comment='城市')
    is_expire = Column(Boolean, default=False, comment='过期标识')

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
