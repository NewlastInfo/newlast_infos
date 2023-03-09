#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import time
import dateparser
import asyncio
import requests
import pymysql
from loguru import logger
from lxml import etree

url = "https://xl.16888.com/ranking-1.html"
url = "https://xl.16888.com/ranking-1.html"
# url = "https://xl.16888.com/brand.html"

headers = {

    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",

}

response = requests.get(url=url, headers=headers).text
print(response)
html = etree.HTML(response)
html_infos = html.xpath('//table[@class="xl-table-def xl-table-a"]/tr')

print(html_infos)
print(len(html_infos))
for html_info in html_infos[:1]:
    ranking_name = ''.join(html_info.xpath('.//th[1]//text()')).strip()
    product_name = ''.join(html_info.xpath('.//th[2]//text()')).strip()
    level_name = ''.join(html_info.xpath('.//th[3]//text()')).strip()
    new_sell_count_name = ''.join(html_info.xpath('.//th[4]//text()')).strip()
    old_sell_count_name = ''.join(html_info.xpath('.//th[5]//text()')).strip()
    rise_rate_name = ''.join(html_info.xpath('.//th[6]//text()')).strip()

for html_info in html_infos[1:]:
    ranking = ''.join(html_info.xpath('.//td[1]//text()')).strip()
    product = ''.join(html_info.xpath('.//td[2]//text()')).strip()
    level = ''.join(html_info.xpath('.//td[3]//text()')).strip()
    new_sell_count = ''.join(html_info.xpath('.//td[4]//text()')).strip()
    old_sell_count = ''.join(html_info.xpath('.//td[5]//text()')).strip()
    rise_rate = ''.join(html_info.xpath('.//td[6]//text()')).strip()

    a = 1
