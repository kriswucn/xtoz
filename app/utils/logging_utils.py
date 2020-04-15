# coding:utf-8
"""
@company: qwgas
@author: kris
@usage: 日志工具类和日志装饰器类
@created: 2019/10/18
"""
import logging
import time
import os
from app import app


class Logger:
    def __init__(self, logger, cmd_level=logging.INFO, file_level=logging.DEBUG):
        try:
            self.logger = logging.getLogger(logger)
            self.logger.setLevel(file_level)
            fmt = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
            current_time = time.strftime('%Y-%m-%d')

            log_dir = app.config.get('LOG_DIR')

            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            self.LogFileName = os.path.join(log_dir, current_time + '.log')
            fh = logging.FileHandler(self.LogFileName)
            fh.setFormatter(fmt)
            fh.setLevel(file_level)
            self.logger.addHandler(fh)
            sh = logging.StreamHandler()
            sh.setLevel(cmd_level)
            self.logger.addHandler(sh)
        except Exception as e:
            raise e


# logger = Logger(__name__, cmd_level=logging.INFO, file_level=logging.INFO)


# 打印日志装饰器
# 目前只支持作为函数装饰器，对类的方法装饰无效
'''
class setlog(object):
    def __init__(self, func):
        self.__func = func

    def __call__(self, *args, **kwargs):
        try:
            start = time.time()
            logger.logger.debug('args参数: %s |  kwargs参数: %s' % (args, kwargs))
            f = self.__func(*args, **kwargs)
            end = time.time()
            duration = (end - start) * 1000
            logger.logger.info('调用[%s]成功，耗时: %.2fms' % (self.__func.__name__, duration))
            return f

        except Exception as e:
            logger.logger.error('调用[%s]失败!' % self.__func.__name__)
            logger.logger.error(e)
            raise e
'''