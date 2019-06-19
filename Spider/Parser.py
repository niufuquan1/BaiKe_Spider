#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 21:25
# @Author  : nfuquan
# @File    : Parser.py
# @Software: PyCharm
import re
from urllib.parse import urljoin

from DownLoader import *
from bs4 import BeautifulSoup


class Parser(object):

    def parsePageForUrl(self, baseUrl, htmlCont, deep):
        '''
        用于解析网页url
        :param baseUrl:网页的基本链接
        :param htmlCont:网页内容
        :param deep:解析深度
        :return:返回url
        '''
        print("进入parsePageForUrl")
        if baseUrl is None or htmlCont is None:
            print(baseUrl is None)
            print(htmlCont is None)
            return
        try:
            nextUrls = set()#下一层深度的url集合
            totalNewUrls = set()#一共的url
            urls = self.getNewUrls(baseUrl, htmlCont)
            totalNewUrls = totalNewUrls | urls
            #print(urls)
            while (deep != 1):
                deep -= 1
                for url in urls:
                    print(url)
                    _htmlCont = DownLoader().getNextPage(url=url)#解析每一个url的网页内容
                    #print(_htmlCont)
                    tempUrls = self.getNewUrls(pageUrl=baseUrl,htmlCont=_htmlCont)#获取内容中的url
                    nextUrls = nextUrls | tempUrls#将获取的url去重添加到下一层深度的url集合中
                #print("从循环中出来了")
                urls = nextUrls#如果深度未到1，将提取到的新的url集合作为输入继续添加新的url
                totalNewUrls = totalNewUrls | nextUrls  # 将获取到的url添加到最后要返回的url集合中
            #print("从while中出来了")
            return totalNewUrls
        except Exception as e:
            print(e)
            return

    def parsePageForData(self, pageUrl, htmlCont):
        '''
        用于解析网页数据
        :param pageUrl:网页的整体链接
        :param htmlCont:网页内容
        :return:返回数据
        '''
        if pageUrl is None or htmlCont is None:
            return
        try:
            newData = self.getNewData(pageUrl, htmlCont)
            return newData
        except Exception as e:
            print(e)

    def getNewUrls(self, pageUrl, htmlCont):
        '''
        通过指定，获取新的链接
        :param pageUrl: 页面的url
        :param htmlCont:网页内容
        :return: 一个新的url集合
        '''
        #print("进入getNewUrls了")
        try:
            newUrls = set()
            soup = BeautifulSoup(htmlCont, 'html.parser', from_encoding='utf-8')
            urls = soup.find_all('a', href=re.compile(r'/item/*'))
            #print(urls)
            for url in urls:
                # 找到相对url地址
                newUrl = url['href']
                # 拼接成完整地址
                newFullUrl = urljoin(pageUrl, newUrl)
                # print(newFullUrl)
                newUrls.add(newFullUrl)
            print("获取url链接完毕，准备返回给nextUrl")
            return newUrls
        except Exception as e:
            print(e)

    def getNewData(self, pageUrl, htmlCont):
        '''
        获取有效数据
        :param pageUrl:网页url
        :param htmlCont:网页源码
        :return:返回有效数据
        '''
        # data为一个字典型数据，键名有url、title、summary
        soup = BeautifulSoup(htmlCont, 'html.parser', from_encoding='utf-8')
        #print(htmlCont)
        try:
            data = {}
            data['url'] = pageUrl
            title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1').get_text()
            data['title'] = title
            summary = soup.find(name='div', attrs={"class":"lemma-summary"}).get_text()
            data['summary'] = summary
            return data
        except Exception as e:
            print(e)
