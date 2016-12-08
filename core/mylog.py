#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import settings


logging.config.dictConfig(settings.LOGGING_DIC)  # 导入上面定义的配置
logger = logging.getLogger(__name__)  # 生成一个log实例
logger.info('It works!')  # 记录该文件的运行状态
