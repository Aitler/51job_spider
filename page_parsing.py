#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: Jan
@software: PyCharm Community Edition
@time: 2016/2/15 17:18
"""

from bs4 import BeautifulSoup
import requests
import time
import json
import pymongo

client = pymongo.MongoClient('localhost', 27017)    # 连接Mongodb创建数据库及相应的表
qiancheng = client['qiancheng']
url_list = qiancheng['url_list']
item_info = qiancheng['item_info']

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
    'Connection': 'keep-alive'
}


# spider1：爬取详情页链接并存入数据库
def get_link_from(city, pages):
    list_view = 'http://m.51job.com/search/joblist.php?jobarea={}&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&from=index&pageno={}'.format(
            str(city),
            str(pages))
    wb_data = requests.get(list_view, headers=headers)    # 请求获得相应网页，headers是告诉服务器我们的身份
    soup = BeautifulSoup(wb_data.text, 'lxml')            # 解析网页
    time.sleep(2)

    if soup.find('div', 'jblist'):
        for link in soup.select('div.jblist a'):         # 获取对于元素url
            item_link = link.get('href')
            url_list.insert_one({'url': item_link})       # 数据存到Mongodb
            print item_link
    else:
        pass


# get_link_from(030200, 2)


# spider2：从详情页链接或许详细信息
def get_item_info(url):
    try:
        wb_data = requests.get(url, headers=headers)
        wb_data.encoding = 'utf-8'
        soup = BeautifulSoup(wb_data.text, 'lxml')
        no_longer_exist = soup.find('p', 'no_record')    # 404页面处理，找不到则pass

        if no_longer_exist:
            pass
        else:
            job_title = soup.select('h1.ltle')[0].text
            company_name = soup.select('a.i.cp.blin')[0].text
            company_nature = soup.select('font.c_ashy')[0].text
            release_time = soup.select('font.c_ashy')[1].text
            pay = soup.select('font.c_ashy')[2].text
            site = soup.select('font.c_ashy')[3].text
            limit = soup.select('font.c_ashy')[4].text.replace('|', '').split()
            location = soup.select('p.jc_msg.word')[0].text.strip()

            if u'职位标签' in soup.select('span.c_dark')[1].text:        # 因为网页结构的问题，当没有职位标签则None
                label = soup.select('div.wbox.word')[0].text.split()
            else:
                label = None

            if u'福利待遇' in soup.select('span.c_dark')[1].text:
                treatment = soup.select('div.wbox.word')[0].text.split()
            else:
                try:
                    treatment = soup.select('div.wbox.word')[1].text.split()
                except:
                    treatment = None

            item_info.insert_one(
                    {'job_title': job_title,
                     'company_name': company_name,
                     'company_nature': company_nature,
                     'release_time': release_time,
                     'pay': pay,
                     'site': site,
                     'limit': limit,
                     'location': location,
                     'label': label,
                     'treatment': treatment,
                     'url': url}
            )

            print job_title, company_name, company_nature, release_time, pay, site, location
            # print json.dumps(limit, encoding='utf-8', ensure_ascii=False)
            # print json.dumps(label, encoding='utf-8', ensure_ascii=False)
            # print json.dumps(treatment, encoding='utf-8', ensure_ascii=False)

    except Exception, e:
        print Exception, ":", e

# get_item_info('http://m.51job.com/search/jobdetail.php?jobid=74788769')
# get_item_info('http://m.51job.com/search/jobdetail.php?jobid=71500000')
# get_item_info('http://m.51job.com/search/jobdetail.php?jobid=74655131')
# get_item_info('http://m.51job.com/search/jobdetail.php?jobid=74870255')
