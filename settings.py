#!  /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)

# 课程配置
COURSES = {
    "Python": {
        "cycle": {
            "min": 24,
            "max": 52
        },
        "price": {
            "min": 6500,
            "max": 24000
        },
        "salary": {
            "min": 18000,
            "max": 50000
        },
        "location": ["beijing"]
    },
    "Linux": {
        "cycle": {
            "min": 12,
            "max": 36
        },
        "price": {
            "min": 4000,
            "max": 18000
        },
        "salary": {
            "min": 15000,
            "max": 60000
        },
        "location": ["beijing"]
    },
    "Golang": {
        "cycle": {
            "min": 24,
            "max": 52
        },
        "price": {
            "min": 5500,
            "max": 26000
        },
        "salary": {
            "min": 20000,
            "max": 65000
        },
        "location": ["shanghai"]
    }
}

CLASSES_MAX_STUDENTS = 80

# 定义三种日志输出格式 开始

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d]\
                   [task_id:%(name)s][%(filename)s:%(lineno)d]\
                   [%(levelname)s][%(message)s]'.replace(' ', '')

simple_format = '[%(levelname)s]\
                 [%(asctime)s]\
                 [%(filename)s:%(lineno)d]\
                 %(message)s'.replace(' ', '')

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'.replace(' ', '')

# 定义日志输出格式 结束

logfile_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'logs')  # log文件的目录

logfile_name = 'school.log'  # log文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        '': {
            # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
