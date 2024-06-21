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

# 获取号码
token = '92b1b328f2e0455d8beeaf46ba6135d2'  # 长期有效
phone_lst = []
phone_lst2 = []
i = 1
cardType = '实卡'
while True:
    if i >= 2:
        break
    get_phone_url = f'http://api.eomsg.com/zc/data.php?code=getPhone&token={token}&cardType={cardType}'
    response = requests.get(get_phone_url)
    # print(response.text)
    phone_number = response.text
    if phone_number.startswith('19'):
        true = 1
        phone_lst.append(phone_number)
        phone_lst2.append(phone_number)
        print(f'phone_number:  {response.text}')
        i += 1
    else:
        pass
        # i -= 1
        # print(f'                                                                        存在电话号码:  {response.text}')

time.sleep(15)
# 获取短信
key_word = '爱回收'

for phone in phone_lst:
    get_msg_url = f'http://api.eomsg.com/zc/data.php?code=getMsg&token={token}&phone={phone}&keyWord={key_word}'
    for i in range(5):
        response = requests.get(url=get_msg_url).text
        # print(response)
        if f'验证码' in response:
            phone_code = ''.join(re.compile(f'验证码是：(.*?)，', re.S).findall(response)).strip()
            print(f'电话号码: {phone}   注册的验证码： {phone_code}')
            # print()
            phone_lst.remove(phone)
            break
        # else:
        # print(f'phone_number: {phone_number}  无验证码')
        # print()
        time.sleep(5)

i = 2
print()
time.sleep(100)
print(f'修改号码:{phone_lst2}，可以点了')
while True:
    i += 1
    for phone in phone_lst2:
        get_msg_url = f'http://api.eomsg.com/zc/data.php?code=getMsg&token={token}&phone={phone}&keyWord={key_word}'
        response = requests.get(url=get_msg_url).text
        # print(response)
        # 19354875291 / 0.16 /【爱回收】您的验证码是：364804，如非本人操作，请忽略此信息。
        if f'验证码' in response:
            phone_code = ''.join(re.compile(f'验证码是：(.*?)，如非', re.S).findall(response)).strip()
            print(f'phone: {phone}   修改密码的验证码： {phone_code}')
            # print()
            phone_lst2.remove(phone)
            # break
        else:
            # print(response)
            time.sleep(2)
            pass
