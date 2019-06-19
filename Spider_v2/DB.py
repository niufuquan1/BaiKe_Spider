#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 21:25
# @Author  : nfuquan
# @File    : DB.py
# @Software: PyCharm
import Log
import pymongo
from settings import *


class Db(object):
    '''
    >>> opts = {'loglevel':3,'logfile':'docTest'}
    >>> db = Db(opts)
    >>> data = {'title':'_DocTest_','Summary':'Test'}
    >>> db.saveToMongoDB(data)
    '''

    def __init__(self, opts):
        self.logger = Log.Logger(opts)
        try:
            self.client = pymongo.MongoClient(MONGO_URL)
            self.db = self.client[MONGO_DB]
        except Exception as e:
            self.logger.toLog(e)
            print("数据库初始化错误！")

    def saveToMongoDB(self, data):
        title = data['title']
        try:
            self.db[title].insert(data)
        except Exception as e:
            self.logger.toLog(e)
            print("存储失败")


if __name__ == '__main__':
    import doctest

    doctest.testmod()
