#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: Jan
@software: PyCharm Community Edition
@time: 2016/2/15 17:06
"""

from bs4 import BeautifulSoup

# 因城市编码需要点击的时候才能加载到网页，故存在本地来处理
path = 'D:/QCjob/city.html'

# 获取城市编码
def city_lists():
    with open(path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        citys = soup.select('tr td')
        for city in citys:
            print city.get('value')

# city_lists()

# 将列表取出来后方便后面使用
city_list = '''
    010000
    020000
    030200
    040000
    180200
    090200
    070200
    050000
    060000
    200200
    080200
'''
