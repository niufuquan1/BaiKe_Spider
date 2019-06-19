#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 21:25
# @Author  : nfuquan
# @File    : UrlManager.py
# @Software: PyCharm
class UrlManager(object):
    def __init__(self):
        self.newUrls = set()
        self.oldUrls = set()

    # 判断是否存在未爬取的url
    def hasNewUrl(self):
        return self.newUrlSize() != 0

    # 获取一个未爬取的url
    def getNewUrl(self):
        newUrl = self.newUrls.pop()
        self.oldUrls.add(newUrl)
        return newUrl

    # 将一个新的url添加到未爬取的URL集合中
    def addNewUrl(self, url):
        if url is None:
            return
        if url not in self.newUrls and url not in self.oldUrls:
            self.newUrls.add(url)

    # 将多个url添加到未爬取的url集合中
    def addNewUrls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.newUrls.add(url)

    # 获取未爬取url集合的大小
    def newUrlSize(self):
        return len(self.newUrls)

    # 获取已经爬取的url集合的大小
    def oldUrlSize(self):
        return len(self.oldUrls)







