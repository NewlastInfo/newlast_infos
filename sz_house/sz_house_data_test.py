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
    "Cookie": "browserDetectorTips=1; apache=bbfde8c184f3e1c6074ffab28a313c87; lss=f7cb2cf4b1607aec30e411e90d47c685; _ulta_id.CM-Prod.e9dc=85f7316f92da84d6; _ulta_ses.CM-Prod.e9dc=ebd65b0ad4aaaebe; isLogin=0; AlteonP10=Ag1xPyw/F6xvdzR2bO1oeA$$",
    "Host": "www.chinamoney.com.cn",
    "If-Modified-Since": "Wed, 11 Jan 2023 06:59:03 GMT",
    "If-None-Match": "3c79-5f1f7891ae070",
    "Referer": "https://www.hao123.com/link/https/?key=http%3A%2F%2Fwww.chinamoney.com.cn%2Fchinese%2Findex.html&&monkey=m-site&c=F75C5209885E8EDD343CD29F32976FE6",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",

}

response = requests.get(url=url, headers=headers)
print(response.text)
