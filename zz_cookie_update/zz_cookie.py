#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from time import sleep
from lxml import etree
from selenium.webdriver.chrome.options import Options  # => 引入Chrome的配置
import redis
import json
import datetime
from selenium.webdriver import ChromeOptions


class ZljSellerPrice:
    cookie_key_sort = {1: 'lon', 2: 'lat', 3: 'idzz', 4: 't', 5: 'zz_t', 6: 'tk', 7: 'id58', 8: 'from',
                       9: 'referrerObj', 10: 'zpm', 11: 'expires', 12: 'zzVisitStack'}

    # 配置
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("lang=zh_CN.UTF-8")

    """ 实现规避检测 """
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 添加参数
    driver = webdriver.Chrome(chrome_options=chrome_options, options=option)

    def time_is_true(self):
        try:
            year = repr(datetime.datetime.now().year)
            month = repr(datetime.datetime.now().month)
            day = repr(datetime.datetime.now().day)
            hour = int(repr(datetime.datetime.now().hour)) + 8
            # hour = int(repr(datetime.datetime.now().hour))
            year_month_day = year + month + day
            week_what = int(datetime.datetime.strptime(year_month_day, "%Y%m%d").weekday() + 1)
            if 10 <= hour <= 20:
                return True
            return False
        except Exception:
            return False

    def get_zz_cookie(self):
        time_is_true = self.time_is_true()
        if time_is_true:
            url = 'https://m.zhuanzhuan.com/u/bmmain/helpsale/evaluate?channel=BM_DEFAULTINDEX&cateId=101&brandId=10530&modelId=58384&usageId=595&preQcCode=1544627318037677082&evaPlanType=B'
            print(url)
            self.driver.get(url)

            sleep(1)
            self.driver.find_element_by_xpath('//button[contains(@class,"btn z-button")]').click()
            sleep(1)
            cookie = self.driver.get_cookies()
            cookie_lst = []
            cookie_dict = dict()

            for cookie_data in cookie:
                cookie_name = cookie_data.get('name')
                cookie_value = cookie_data.get('value')
                for key, value in self.cookie_key_sort.items():
                    if value == cookie_name:
                        cookie_str = f'{cookie_name}={cookie_value}'
                        cookie_lst.append(cookie_str)
                        cookie_dict[key] = cookie_str

            cookie_str_dict = {}
            for i in range(12):
                cookie_str_dict[i + 1] = cookie_dict[i + 1]

            # cookie_str_dict[10] = 'zpm=4^A5341^1^0^0'
            cookie_str_dict[8] = 'from=5^T1082^1^0^0'
            cookie_str = '; '.join(list(cookie_str_dict.values()))
            print('cookie_str:', cookie_str)

            zz_cookie_name = "token:accounts:zz_cookie"
            prod_r = redis.Redis(host='193.112.98.154', password='d2hvYW1pOmlhbXdobw==', db=6, decode_responses=True)
            prod_r.hdel(zz_cookie_name, "zz_cookie")
            prod_r.hset(zz_cookie_name, "zz_cookie", cookie_str)

            self.driver.delete_all_cookies()
            # driver.close()
        else:
            time.sleep(60)


if __name__ == '__main__':

    while True:
        try:
            st = time.time()
            ZljSellerPrice().get_zz_cookie()
            et = time.time()
            print(f'消耗时间为:{et - st}')
            # print(f'第{i + 1}次获取cookie')
            print()
        except Exception:
            pass
