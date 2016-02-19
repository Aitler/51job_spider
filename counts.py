#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: Jan
@software: PyCharm Community Edition
@time: 2016/2/15 21:21
"""

import time
from page_parsing import url_list, item_info

# 每5秒查询表的记录数
while True:
    url_counts = url_list.find().count()
    info_counts = item_info.find().count()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print str(url_counts) + '  ' + str(info_counts) + '  ' + str(now_time)
    time.sleep(5)
