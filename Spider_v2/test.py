#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 19:48
# @Author  : nfuquan
# @File    : test.py
# @Software: PyCharm
import os


def Test(object):
    '''


    '''
    tests = ["DownLoader.py", "Parser.py", "DB.py"]

    for test in tests:
        result =os.popen("python %s" % test).read()
        print(result)

if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose=True))