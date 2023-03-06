#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import time
import requests
import pymysql
from loguru import logger
from dingTalk_cny import DingTalks
from settings import *
from lxml import etree


class CnyToOthersInfo:
    # session = AioRequests()
    ke_head_url = 'https://36kr.com'

    mysql_host = MYSQL_HOST
    mysql_user = MYSQL_USER
    mysql_port = MYSQL_PORT
    mysql_password = MYSQL_PASSWORD
    mysql_databases = MYSQL_DATABASES

    @logger.catch  # 添加日志装饰器，自动将代码异常处记录
    def get_req_params(self):
        url = "https://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/ccpr.json?t=1678085144679"
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
        req_params = dict(
            url=url,
            headers=headers,
            method='GET'
        )
        return req_params

    def get_cny_info(self):
        req_params = self.get_req_params()
        response = requests.get(url=req_params.get('url'), headers=req_params.get('headers')).json()
        response_json = response.get('records')
        lastDate = response.get('data').get('lastDate')
        for response_data in response_json:
            price = response_data.get('price')
            vrtName = response_data.get('vrtName')
            time_str = lastDate
            tuple_sql = (vrtName, price, time_str,)
            # print(tuple_sql)
            self.insert_ke_data(tuple_sql)
        time.sleep(60 * 60 * 10)

    def insert_ke_data(self, tuple_sql: tuple):
        """
        1、20220105新增MySQL存储
        2、存储各个渠道的价格历史数据
        :param data:
        :param current_key:
        :return:
        """
        try:
            conn = pymysql.connect(
                host=self.mysql_host,
                user=self.mysql_user,
                port=self.mysql_port,
                password=self.mysql_password,
                database=self.mysql_databases
            )
            cursor = conn.cursor()
            try:
                insert_sql = """insert into cny_to_others(vrtName, price, time_str) values (%s,%s,%s) """
                # 执行 存储语句
                cursor.execute(insert_sql, tuple_sql)
                conn.commit()
                conn.close()
                vrtName, price, time_str = tuple_sql
                message = f'币种：{vrtName};\n汇率：{price};\n时间：{time_str};'
                print(message)
                DingTalks.compose(message)
            except Exception as e:
                print(e)
                conn.close()
                pass
        except Exception as w:
            print(w)
            pass


def cny_main():
    while True:
        try:
            CnyToOthersInfo().get_cny_info()
        except Exception as e:
            pass


if __name__ == '__main__':
    cny_main()
