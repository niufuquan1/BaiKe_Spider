#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 21:27
# @Author  : nfuquan
# @File    : DownLoader.py
# @Software: PyCharm
from urllib.parse import urljoin

import Log
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings import *


class DownLoader(object):
    '''
    >>> opts = {'url':'https://baike.baidu.com/item/Python/407313','loglevel':3,'logfile':'docTest'}
    >>> downloader = DownLoader(opts)
    >>> pageSource = downloader.getNextPage(url=opts['url'])
    >>> print(pageSource != None)
    True

    '''

    def __init__(self, opts):
        self.logger = Log.Logger(opts)

    def getFirstWebPage(self, keyword, url):
        browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        wait = WebDriverWait(browser, 10)
        print("正在搜索")
        try:
            browser.get(url)
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#query"))
            )
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search')))
            input.send_keys(keyword)
            submit.click()
            # pageSourceTotal = wait.until(
            #   EC.presence_of_element_located((By.CSS_SELECTOR,
            #                                    'body > div.body-wrapper.feature.feature_small.collegeSmall > div.feature_poster > div')))

            pageSource = browser.page_source
            return pageSource
        except TimeoutException as e:
            self.logger.toLog(e)
            print("TimeOut")
            return self.getFirstWebPage()
        except StaleElementReferenceException as e:
            self.logger.toLog(e)
            return self.getFirstWebPage()

    def getNextPage(self, url):
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
            }
            response = requests.get(url, headers=header, allow_redirects=False)
            if response.status_code == 302 or response.status_code == 301:
                redirectUrl = response.headers['location']
                # 拼接成完整地址
                newFullUrl = urljoin("https://baike.baidu.com", redirectUrl)
                response = requests.get(newFullUrl, headers=header, allow_redirects=False)
                response.encoding = 'utf-8'
                return response.text
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
        except Exception as e:
            self.logger.toLog(e)
            print("请求出错")


if __name__ == '__main__':
    # opts = {'url': 'https://baike.baidu.com/', 'loglevel': 3, 'logfile': 'docTest', 'keyword': 'python'}
    # downloader = DownLoader(opts)
    # pageSource = downloader.getFirstWebPage(keyword=opts['keyword'], url=opts['url'])
    # print(pageSource)
    import doctest
    doctest.testmod()
