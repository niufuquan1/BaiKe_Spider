#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/20 13:14
# @Author  : nfuquan
# @File    : BaiKeSpider.py
# @Software: PyCharm
import argparse
import logging
import os
import queue
import re
import sys
import threading
import time
import traceback
from urllib.parse import urljoin
import pymongo
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging.handlers

defaultUrl = "https://baike.baidu.com/"
defaultDeep = 1
MONGO_URL = 'localhost'
MONGO_DB = 'BaiKe'
LOGGER = logging.getLogger('Spider')  # 设置logging模块的前缀
LEVELS = {
    1: 'DEBUG',
    2: 'INFO',
    3: 'WARNING',
    4: 'ERROR',
    5: 'CRITICAL'
}
formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')  # 自定义日志格式
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
lock = threading.Lock()  # 设置线程锁


class Logger(object):
    def __init__(self, logfile):
        self.logfile = logfile

    def configLogger(self):
        '''
        配置日志文件和记录等级
        :return:
        '''
        try:
            # 创建文件目录
            logs_dir = self.logfile
            if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
                pass
            else:
                os.mkdir(logs_dir)
                # 修改log保存位置
            timestamp = time.strftime("%Y-%m-%d", time.localtime())
            logfilename = '%s.txt' % timestamp
            logfilepath = os.path.join(logs_dir, logfilename)
            handler = logging.handlers.RotatingFileHandler(filename=logfilepath,
                                                           maxBytes=10240000,  # 文件最大字节数
                                                           backupCount=5,  # 会轮转5个文件，共6个
                                                           encoding='gbk'
                                                           )
        except IOError as e:
            print(e)
            return -1
        else:
            handler.setFormatter(formatter)  # 设置日志格式
            LOGGER.addHandler(handler)  # 增加处理器
            logging.basicConfig(level=logging.NOTSET)  # 设置,不打印小于4级别的日志
        return LOGGER  # 返回logging实例

class MongoDB(object):
    def __init__(self, opts, logger):
        self.opts = opts
        self.logger = logger
        self.loglevel = opts.loglevel
        try:
            self.client = pymongo.MongoClient(MONGO_URL)
            self.db = self.client[MONGO_DB]
        except Exception as e:
            toLogger(logger, self.loglevel, e, True)
            return -1

    def saveToMongoDB(self, data):
        title = data['title']
        try:
            self.db[title].insert_one(data)
        except Exception as e:
            toLogger(self.logger, self.loglevel, e, True)


class Spider(object):
    '''
    >>> logger = Logger('test').configLogger()
    >>> tp  = ThreadPool(5)
    >>> def c():pass
    >>> c.deep = 1
    >>> c.logfile = '_test'
    >>> c.loglevel = 1
    >>> c.keyword = 'uestc'
    >>> c.url = 'https://baike.baidu.com/'
    >>> s = Spider(c,tp,logger)
    >>> s.getPageContent(c.url,c.keyword,c.deep,True)
    True
    '''
    def __init__(self, opts, tp, logger):
        self.deep = opts.deep  # 指定网页的抓取深度
        self.url = opts.url  # 指定网站url
        self.keyword = opts.keyword  # 要搜索的关键字
        self.logfile = opts.logfile  # 日志文件路径和名字
        self.loglevel = opts.loglevel  # 日志级别
        self.tp = tp  # 连接池回调实例
        self.logger = logger  # logging模块实例
        self.haveUrls = []  # 抓取的网页放入列表,防止重复抓取
        self.opts = opts
        self.encoding = 'utf-8'

    def _hasGraber(self, url):
        '''
        判断是否已经抓取过这个页面
        :param url:传入的url
        :return:
        '''
        return (True if url in self.haveUrls else False)

    def getPageContent(self, url, keyword, deep, flag):
        '''
        抓页面，然后分析，最后持久化
        :param url:需要抓取的url
        :param keyword:查询关键字
        :param deep:深度
        :param flag:标记，用于判断是否是第一次通过url获取,True为第一次，False为其他情况
        :return:
        '''
        if (flag == True):
            browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
            wait = WebDriverWait(browser, 10)
            try:
                browser.get(url)
                input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#query"))
                )
                submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search')))
                input.send_keys(keyword)
                submit.click()
                result = browser.page_source
            except TimeoutException as e:
                toLogger(self.logger, self.loglevel, e, True)
            except StaleElementReferenceException as e:
                toLogger(self.logger, self.loglevel, e, True)
            finally:
                self.flag = False
                browser.close()
        else:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
            }
            # 发现重复的url，直接返回
            if self._hasGraber(url):
                return
            else:
                # 发现是一个新的，未爬取的url，则加入新的列表
                self.haveUrls.append(url)
                try:
                    response = requests.get(url, headers=header, allow_redirects=False)
                    response.encoding = 'utf-8'
                    result = response.text
                except requests.HTTPError as e:
                    toLogger(self.logger, self.loglevel, e, True)
                    return -1

        if self.loglevel > 3:
            toLogger(self.logger, self.loglevel, '抓取网页 %s 成功' % url)
        try:
            self.parse(url, result, keyword, deep)  # 分析页面中的url,持久化网页的内容
        except Exception as e:
            toLogger(self.logger, self.loglevel, e, True)
            return -1
        else:
            if self.loglevel > 3:
                toLogger(self.logger, self.loglevel, '分析网页 % s成功' % url)
        return True

    def parse(self, url, htmlCont, keyword, deep):
        db = MongoDB(self.opts, self.logger)

        soup = BeautifulSoup(htmlCont, 'html.parser')
        urls = soup.find_all('a', href=re.compile(r'/item/*'))
        if deep > 1:
            for _url in urls:
                # 找到相对url地址
                newUrl = _url['href']
                # 拼接成完整地址
                newFullUrl = urljoin("https://baike.baidu.com/", newUrl)
                self.tp.addJob(self.getPageContent, url=newFullUrl, keyword=keyword, deep=deep - 1,
                               flag=False)  # 递归调用,直到符合的深度
        data = {}
        data['url'] = url
        title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1').get_text()
        data['title'] = title
        summary = soup.find(name='div', attrs={"class": "lemma-summary"}).get_text()
        data['summary'] = summary
        db.saveToMongoDB(data)

    def work(self):
        self.tp.addJob(self.getPageContent, url=self.url, keyword=self.keyword, deep=self.deep, flag=True)
        self.tp.waitForComplete()


class SpiderThread(threading.Thread):
    def __init__(self, workQueue, timeOut=60, *kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        self.timeOut = timeOut
        self.setDaemon(True)
        self.workQueue = workQueue
        self.start()

    def run(self):
        while (True):
            try:
                lock.acquire()  # 上锁
                callable, args = self.workQueue.get(timeout=self.timeOut)
                url = args['url']
                keyword = args['keyword']
                deep = args['deep']
                flag = args['flag']
                callable(url, keyword, deep, flag)
                lock.release()
                if (self.workQueue.empty()):  # 队列空了，就结束该线程
                    break
            except Exception as e:
                print(e)


class ThreadPool(object):
    def __init__(self, threadNums):
        self.workQueue = queue.Queue()
        self.threads = []
        self.createThreadPool(threadNums)

    def createThreadPool(self, threadNums):
        for i in range(threadNums):
            thread = SpiderThread(self.workQueue)
            self.threads.append(thread)

    def waitForComplete(self):
        '''
        等待全部线程完毕
        :return:
        '''
        while (len(self.threads)):
            thread = self.threads.pop()
        # 判断线程是否还存活决定是否用join
        if thread.isAlive():
            thread.join()

    def addJob(self, callable, **args):
        '''
        增加任务，放入队列
        :param callable: 函数名
        :param args: 相关参数
        :return:
        '''
        self.workQueue.put((callable, args))


def toLogger(logger, level, message, error=False):
    '''
    记录日志函数
    :param level:等级
    :param message:消息
    :param error:错误标记,为True则标记为错误日志，启动下面的if语句
    :return:无
    '''
    getattr(logger, LEVELS.get(level, 'WARNING').lower())(message)
    if error:  # 当发现是错误日志,还会记录错误的堆栈信息
        getattr(logger, LEVELS.get(level, 'WARNING').lower())(traceback.format_exc())


def argParse():
    parser = argparse.ArgumentParser(description="This is used for spider1's args.")  # 定义解析器
    # action是指存储方式，dest是指显示中将相关参数关联到一个名字上，default是指在不指定该参数的情况下的默认值，type指定输入参数的类型或者对应一个函数进行处理
    parser.add_argument("-u", "-url", action="store", dest="url", default=defaultUrl,
                        help="Input a URL for the Spider. Example:https://www.Google.com")
    parser.add_argument("-d", "-deep", action="store", dest="deep", default=defaultDeep, type=int,
                        help="Input a deep for the Spider. default=1")
    parser.add_argument("-k", "-key", action="store", dest="keyword", help="Input a keyword to search in baike")
    parser.add_argument("-f", "-logfile", action="store", dest="logfile", default="BaiKeSpider",
                        help="Input a logfile name for the Spider. default=BaiKeSpider.log")
    parser.add_argument("-l", "-loglevel", action="store", dest="loglevel", default=1, type=int,
                        help="Input a loglevel for the Spider. default=1")
    parser.add_argument("-t", "-threadnumber", action="store", dest="threadnumber", default=5, type=int,
                        help="Input a threadnumber for the Spider. default=5")
    parser.add_argument("-s", "-testself", dest="testself", action="store_true",
                        help="Test the Spider. default=False", default=False)
    opts = parser.parse_args()  # 这里相当于解析传过来的参数，并将结果放在opts中
    return opts


def main():
    '''
    主函数
    :return: 
    '''
    try:
        # 解析参数
        opts = argParse()
        # 如果testself,执行doctest
        if opts.testself:
            import doctest
            doctest.testmod()
            return
        # 判断关键词是否存在
        if not opts.keyword:
            print("Need a KeyWord for the Spider!")
            return
            # 实例化爬虫类,并启动调度器
        logger = Logger(opts.logfile).configLogger()  # 实例化日志调用
        tp = ThreadPool(opts.threadnumber)
        spider = Spider(opts, tp, logger)
        spider.work()  # 主方法
    except KeyboardInterrupt:
        print("\rBye~")
        sys.exit(0)


if __name__ == '__main__':
    main()
