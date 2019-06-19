#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 14:32
# @Author  : nfuquan
# @File    : Log.py
# @Software: PyCharm

# 默认的配置
import logging
import logging.handlers
import os
import time


class Logger(object):
    def __init__(self, opts):
        # 获取对象
        self.logger = logging.getLogger("")
        self.opts = opts
        # 设置输出的等级
        LEVELS = {
            1: logging.DEBUG,
            2: logging.INFO,
            3: logging.WARNING,
            4: logging.ERROR,
            5: logging.CRITICAL}
        # 创建文件目录
        if (type(self.opts).__name__ == 'dict'):
            #判断是否是doctest传过来的参数
            logs_dir = self.opts['logfile']
        else:
            logs_dir = self.opts.logfile  # "BaiKeSpiderLog"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.txt' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
                                                                   maxBytes=1024 * 1024 * 50,
                                                                   backupCount=5)
        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        rotatingFileHandler.setFormatter(formatter)
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.NOTSET)
        console.setFormatter(formatter)
        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.NOTSET)

    def toLog(self, message):
        if(type(self.opts).__name__ == 'dict'):
            level = self.opts['loglevel']
        else:
            level = self.opts.loglevel

        if (level == 1):
            self.logger.debug(message)
        elif (level == 2):
            self.logger.info(message)
        elif (level == 3):
            self.logger.warning(message)
        elif (level == 4):
            self.logger.error(message)
        elif (level == 5):
            self.logger.critical(message)
