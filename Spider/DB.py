#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 21:25
# @Author  : nfuquan
# @File    : DB.py
# @Software: PyCharm
import pymongo

from settings import *


class Db(object):
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_URL)
            self.db = self.client[MONGO_DB]
        except Exception as e:
            print("数据库初始化错误！")

    def saveToMongoDB(self, data):
        title = data['title']
        try:
            if self.db[title].insert(data):
                print("保存成功")
        except Exception:
            print("存储失败")
