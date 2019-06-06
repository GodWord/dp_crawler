# -*- coding:utf-8 -*-
import logging.config
import os

from setting.config import BASE_DIR

LOG_PATH = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

LOGGING = {
    # 基本设置
    'version': 1,  # 日志级别
    'disable_existing_loggers': False,  # 是否禁用现有的记录器

    # 日志格式集合
    'formatters': {
        # 标准输出格式
        'standard': {
            'format': '%(levelname)s [%(asctime)s][%(pathname)s %(module)s(%(lineno)d):%(funcName)s]:%(message)s'
        }
    },

    # 过滤器
    'filters': {
        # 'require_debug_true': {
        #     '()': RequireDebugTrue,
        # }
    },

    # 处理器集合
    'handlers': {
        # 输出到控制台
        'console': {
            'level': 'DEBUG',  # 输出信息的最低级别
            'class': 'logging.StreamHandler',
            'formatter': 'standard',  # 使用standard格式
            # 'filters': ['require_debug_true', ],  # 仅当 DEBUG = True 该处理器才生效
        },
        # 输出到文件
        'all': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # ConcurrentRotatingFileHandler
            'formatter': 'standard',
            'filename': os.path.join(LOG_PATH, 'all.log'),  # 输出位置
            'maxBytes': 1024 * 1024 * 100,  # 文件大小 100M
            'backupCount': 10,  # 备份份数
            'encoding': 'utf8',  # 文件编码
        },
        # 输出到文件
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # ConcurrentRotatingFileHandler
            'formatter': 'standard',
            'filename': os.path.join(LOG_PATH, 'error.log'),  # 输出位置
            'maxBytes': 1024 * 1024 * 100,  # 文件大小 100M
            'backupCount': 10,  # 备份份数
            'encoding': 'utf8',  # 文件编码
        },

        # 输出到文件
        'proxy': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # ConcurrentRotatingFileHandler
            'formatter': 'standard',
            'filename': os.path.join(LOG_PATH, 'proxy.log'),  # 输出位置
            'maxBytes': 1024 * 1024 * 100,  # 文件大小 100M
            'backupCount': 10,  # 备份份数
            'encoding': 'utf8',  # 文件编码
        },
        # 输出到文件
        'comment': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # ConcurrentRotatingFileHandler
            'formatter': 'standard',
            'filename': os.path.join(LOG_PATH, 'comment.log'),  # 输出位置
            'maxBytes': 1024 * 1024 * 100,  # 文件大小 100M
            'backupCount': 10,  # 备份份数
            'encoding': 'utf8',  # 文件编码
        },

    },

    # 日志管理器集合
    'loggers': {
        # 管理器
        'default': {
            'handlers': ['console', 'all', 'error'],
            'level': logging.DEBUG,
            'propagate': True,  # 是否传递给父记录器
        },
        'proxy': {
            'handlers': ['console', 'all', 'error', 'proxy'],
            'level': logging.DEBUG,
            'propagate': True,  # 是否传递给父记录器
        },
        'comment': {
            'handlers': ['console', 'all', 'error', 'comment'],
            'level': logging.DEBUG,
            'propagate': True,  # 是否传递给父记录器
        },

    }
}
