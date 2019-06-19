#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 16:25
# @Author  : nfuquan
# @File    : Scheduler.py
# @Software: PyCharm

import argparse
import os
import re

import DB
import DownLoader
import Log
import Parser
import UrlManager
import settings


class Utils(object):
    # 检查url的格式
    def checkUrl(string):
        pattern = re.compile("(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")
        m = pattern.match(string)
        if m == None:
            msg = "%s is not a correct url or missing http|https:// header!" % string
            raise argparse.ArgumentTypeError(msg)
        return string


class ArgParse(object):
    def __init__(self):
        pass

    def argParse(self):
        parser = argparse.ArgumentParser(description="This is used for spider1's args.")  # 定义解析器
        # action是指存储方式，dest是指显示中将相关参数关联到一个名字上，default是指在不指定该参数的情况下的默认值，type指定输入参数的类型或者对应一个函数进行处理
        parser.add_argument("-u", "-url", action="store", dest="url", default=settings.defaultUrl,
                            type=Utils.checkUrl, help="Input a URL for the Spider. Example:https://www.Google.com")
        parser.add_argument("-d", "-deep", action="store", dest="deep", default=settings.defaultDeep, type=int,
                            help="Input a deep for the Spider. default=1")
        parser.add_argument("-k", "-key", action="store", dest="keyword", help="Input a keyword to search in baike")
        parser.add_argument("-f", "-logfile", action="store", dest="logfile", default="BaiKeSpider.log",
                            help="Input a logfile name for the Spider. default=Spider.log")
        parser.add_argument("-l", "-loglevel", action="store", dest="loglevel", default=1, type=int,
                            help="Input a loglevel for the Spider. default=1")
        parser.add_argument("-t", "-threadnumber", action="store", dest="threadnumber", default=5, type=int,
                            help="Input a threadnumber for the Spider. default=5")
        parser.add_argument("-s", "-testself", dest="testself", action="store_true",
                            help="Test the Spider. default=False", default=False)
        opts = parser.parse_args()  # 这里相当于解析传过来的参数，并将结果放在opts中
        print(opts)
        return opts


class Spider(object):
    def __init__(self, opts):
        self.opts = opts
        self.urlmanager = UrlManager.UrlManager()
        self.downloader = DownLoader.DownLoader(opts)
        self.parser = Parser.Parser(opts)
        self.db = DB.Db(opts)
        self.logger = Log.Logger(opts)

    def scheduler(self):
        '''
        爬虫调度器
        :return:无返回
        '''
        # 添加入口的url
        baseUrl = "https://baike.baidu.com"

        try:
            # 赋值入口url
            newUrl = baseUrl
            # 下载第一次的url对应的网页数据
            htmlCont = self.downloader.getFirstWebPage(self.opts.keyword, baseUrl)
            # 解析器抽取网页数据（根据深度已经全部将网页url爬取下来）
            totalUrls = self.parser.parsePageForUrl(baseUrl, htmlCont, self.opts.deep)
            # newData = self.parser.parsePageForData(newUrl, htmlCont)
            # print("出来了")
            # 将抽取的url添加到url管理器中
            self.urlmanager.addNewUrls(totalUrls)
            # 将集合转换为list对象，然后逐个进行解析
            urlList = list(self.urlmanager.newUrls)
            for url in urlList:
                htmlCont = self.downloader.getNextPage(url)
                newData = self.parser.parsePageForData(url, htmlCont)
                if newData == None:
                    print("获取数据为空")
                else:
                    # 数据存储器存储文件
                    self.db.saveToMongoDB(newData)
        except Exception as e:
            self.logger.toLog(e)
            print("Spider failed")


def main():
    # 解析参数
    opts = ArgParse().argParse()
    #如果存在testself,执行testself
    print(type(opts))
    if(opts.testself):
        tests = ["DownLoader.py", "Parser.py", "DB.py"]
        for test in tests:
            result = os.popen("python %s" % test).read()
            print(result)
    # 判断关键词是否存在
    if not opts.keyword:
        print("Need a KeyWord for the Spider!")
        return
    # 实例化爬虫类,并启动调度器
    spider = Spider(opts)
    spider.scheduler()


if __name__ == "__main__":
    main()
