#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: Jan
@software: PyCharm Community Edition
@time: 2016/2/15 20:59
"""

from multiprocessing import Pool
from city_extract import city_list
from page_parsing import get_link_from, get_item_info, url_list, item_info
import time

db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in item_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x - y                                                     # 去重处理
# print rest_of_urls


# 循环获取对应页码url链接，可以根据查询结果来定多少页
def get_all_links_from(city):
    for num in range(1, 31):
        # time.sleep(5)
        get_link_from(city, num)

# 爬虫1主程序，先运行爬虫1再运行爬虫2
if __name__ == '__main__':
    pool = Pool(processes=6)
    pool.map(get_all_links_from, city_list.split())
    pool.close()
    pool.join()

# 爬虫2主程序，取消爬虫2注释的时候要将爬虫1注释掉
# if __name__ == '__main__':
#     pool = Pool(processes=6)
#     pool.map(get_item_info, rest_of_urls)
#     pool.close()
#     pool.join()
