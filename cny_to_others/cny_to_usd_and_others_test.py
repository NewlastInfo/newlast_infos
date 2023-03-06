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

url = "https://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/rfx-sp-quot.json?t=1678084892629&t=1678084912700"
url = "https://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/ccpr.json?t=1678085144679"
# url = 'https://www.cih-index.com/data/house/chengdu.html'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.chinamoney.com.cn",
    "If-Modified-Since": "Wed, 11 Jan 2023 06:59:03 GMT",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

response = requests.get(url=url, headers=headers).json()
response_json = response.get('records')
lastDate = response.get('data').get('lastDate')
for response_data in response_json:
    price = response_data.get('price')
    vrtName = response_data.get('vrtName')
    time_str = lastDate
    print(price, vrtName, time_str)
    break
