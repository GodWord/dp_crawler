# -*- coding:utf-8 -*-
__author__ = 'zhoujifeng'
__date__ = '2019/4/3 19:41'

from datetime import datetime

from sqlalchemy import BigInteger, Column, Integer, String, DateTime, create_engine, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from setting.config import DB_SOURCE

Base = declarative_base()

engine = create_engine(DB_SOURCE['default'], encoding="utf-8", echo=False)


class Cookie(Base):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    __tablename__ = "cookie"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cookie = Column(String(800), nullable=True, comment='cookie')
    city = Column(String(500), nullable=True, comment='城市')
    type = Column(Integer, nullable=True, default=0, comment='PC为0 移动端为1')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


Base.metadata.create_all(engine)  # 创建表结构
