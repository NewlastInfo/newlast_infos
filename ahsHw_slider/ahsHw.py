#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import datetime
import re
import requests
import redis
import pymysql
import random

REDIS_HOST = '193.112.98.154'
REDIS_PASSWORD = 'd2hvYW1pOmlhbXdobw=='
REDIS_DB = 6


class AhsHwCookie(object):
    def __init__(self):
        self.ahsHw_cookie_name = "token:accounts:ahsHw_cookie"

        self.arg_url = "https://vmall-m.aihuishou.com/api/inquiries/create"
        self.price_url = "https://vmall-m.aihuishou.com/api/inquiries/list"

        self.redis_host = REDIS_HOST
        self.redis_password = REDIS_PASSWORD
        self.redis_db = REDIS_DB

    def deal_price_data(self):
        year_month_day = self.get_time_str()
        ahs_hw_cookie_name = f"ahsHw:price:data_info_{year_month_day}"
        prod_r = redis.Redis(host=self.redis_host, password=self.redis_password, db=self.redis_db,
                             decode_responses=True)
        price_data = prod_r.hgetall(ahs_hw_cookie_name)
        for price_info, price_num in price_data.items():
            if not price_num:
                st = time.time()
                self.return_data(price_info)
                et = time.time()
                print(f'消耗时间为{et - st}')
            else:
                time.sleep(1.7)

    def getIpList(self):
        conn = pymysql.connect(host='159.75.235.206', port=7075, user='pajia', password='WKe@YwruhzydqXDFAAVM',
                               database='pajia_server_001_db')
        cursor = conn.cursor()
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        select_sql = "select ip, port, expire_time from pingyi_ip_proxy  where expire_time >= '%s'  limit 20" % now_time
        cursor.execute(select_sql)
        ip_port_expire_time = cursor.fetchall()
        conn.close()
        ip_lst = []
        for ip_port in ip_port_expire_time:
            ip = ip_port[0]
            port = ip_port[1]

            proxies = {'http': 'https://{}'.format(str(ip) + ":" + str(port))}

            ip_lst.append(proxies)
        ip_port = random.choice(ip_lst)
        return ip_port

    def return_cookie(self):
        ahsHw_cookie_name = "token:accounts:ahsHw_cookie"
        prod_r = redis.Redis(host=self.redis_host, password='d2hvYW1pOmlhbXdobw==', db=6, decode_responses=True)
        ahsHw_cookie = prod_r.hget(ahsHw_cookie_name, 'ahsHw_cookie')
        return ahsHw_cookie

    def return_data(self, price_info):

        u_atoken = '0b72f618-4c1-4aba-9a78-f1658998784477ba'
        csessionid = ''
        u_asig = ''
        slider_url = f'https://vmall-m.aihuishou.com/api/inquiries/create?u_atoken={u_atoken}&u_asession={csessionid}&u_asig={u_asig}&u_aref=123'

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7",
            "ahs-agent": "HUAWEI_M",
            "Connection": "keep-alive",
            "Content-Length": "168",
            "Content-Type": "application/json;charset=UTF-8",
            "Host": "vmall-m.aihuishou.com",
            "Origin": "https://vmall-m.aihuishou.com",
            "Referer": "https://vmall-m.aihuishou.com/product/detail/36472",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",

        }

        print(slider_url)
        price_info = json.loads(price_info)
        price_info['productId'] = int(price_info['productId'])
        print('price_info:', price_info)
        price_info = json.dumps(price_info)
        ip_port = self.getIpList()
        response = requests.post(url=slider_url, headers=headers, data=price_info, proxies=ip_port)
        # response = requests.post(url=slider_url, headers=headers, data=price_info)

        print(response.text)
        print(response.status_code)
        price_data = response.json().get('data')
        print('price_data:', price_data)

        data = {"keys": [f"{price_data}"]}
        print()
        return_cookie = self.return_cookie()
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7",
            "ahs-agent": "HUAWEI_M",
            "Connection": "keep-alive",
            "Content-Length": "168",
            "Content-Type": "application/json;charset=UTF-8",
            "Cookie": f"{return_cookie}",
            "Host": "vmall-m.aihuishou.com",
            "Origin": "https://vmall-m.aihuishou.com",
            "Referer": "https://vmall-m.aihuishou.com/product/detail/36472",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }
        ip_port = self.getIpList()
        res = requests.post(url=self.price_url, headers=headers, data=json.dumps(data), proxies=ip_port)
        # res = requests.post(url=self.price_url, headers=headers, data=json.dumps(data))

        try:
            price_num = res.json().get("data")[0].get('price')
        except Exception as e:
            price_num = None
        print('price_num:', price_num)
        if not price_num:
            # print(f'需要更新爱回收华为的cookie了')
            # time.sleep(1000000)
            self.update_price_data(price_info, 'SKU组合不存在')
        else:

            self.update_price_data(price_info, price_num)

    def update_price_data(self, price_info, price_data):
        year_month_day = self.get_time_str()
        ahsHw_cookie_name = f"ahsHw:price:data_info_{year_month_day}"
        prod_r = redis.Redis(host=self.redis_host, password=self.redis_password, db=self.redis_db,
                             decode_responses=True)
        prod_r.hset(ahsHw_cookie_name, price_info, price_data)

    def get_time_str(self) -> str:
        year = repr(datetime.datetime.now().year)
        month_ = datetime.datetime.now().month
        month = repr(month_) if month_ > 9 else '0' + repr(month_)
        day_ = datetime.datetime.now().day
        day = repr(day_) if day_ > 9 else '0' + repr(day_)
        year_month_day = year + month + day
        return year_month_day


if __name__ == '__main__':
    i = 0
    while True:
        try:
            ahs_hw_price = AhsHwCookie()
            ahs_hw_price.deal_price_data()
            i += 1
            if i > 3600 * 2.5:
                print(f'已经消耗了{3600 * 2.5}秒')
                print(f'已经爬价了{3600 * 2.5}次')
                print(f'暂停运行，可能需要更新cookie了')
                # time.sleep(10000000000)
                break


        except Exception:
            continue
