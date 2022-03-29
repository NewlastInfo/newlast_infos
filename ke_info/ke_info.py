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

from dingTalk_ke import DingTalks
from settings import *
from lxml import etree


class KeInfo:
    # session = AioRequests()
    ke_head_url = 'https://36kr.com'

    mysql_host = MYSQL_HOST
    mysql_user = MYSQL_USER
    mysql_port = MYSQL_PORT
    mysql_password = MYSQL_PASSWORD
    mysql_databases = MYSQL_DATABASES

    @logger.catch  # 添加日志装饰器，自动将代码异常处记录
    def get_req_params(self):
        url = "https://36kr.com/information/technology/"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "referer": "https://36kr.com/information/technology/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", }
        req_params = dict(
            url=url,
            headers=headers,
            method='GET'
        )
        return req_params

    def get_36ke_venture_capital(self):
        req_params = self.get_req_params()
        res_code = requests.get(req_params.get('url'), req_params.get('headers')).text
        html = etree.HTML(res_code)
        html_infos = html.xpath(
            '//div[@class="information-flow-list"]//div[@class="article-item-info clearfloat"]')
        print(len(html_infos))
        for html_info in html_infos:
            title = ''.join(html_info.xpath('.//a[contains(@class,"m-title")]//text()')).strip()
            info_url = self.ke_head_url + ''.join(
                html_info.xpath('.//a[contains(@class,"m-title")]/@href')).strip()
            summary = ''.join(html_info.xpath('.//a[contains(@class,"m-description")]//text()')).strip()
            author = ''.join(html_info.xpath('.//a[contains(@class,"author")]//text()')).strip()
            public_time_str = ''.join(html_info.xpath('.//span[contains(@class,"bar-time")]//text()')).strip()
            public_time = str(dateparser.parse(public_time_str)).split('.')[0].strip()
            time.sleep(30)
            tuple_sql = (title, info_url, summary, author, public_time,)
            # print(tuple_sql)
            self.insert_ke_data(tuple_sql)
        time.sleep(60 * 60)

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
                insert_sql = """insert into ke_info(title, info_url, summary, author, public_time) values (%s,%s,%s,%s,%s) """
                # 执行 存储语句
                cursor.execute(insert_sql, tuple_sql)
                conn.commit()
                conn.close()
                title, info_url, summary, author, public_time = tuple_sql
                message = f'标题：{title};\n链接：{info_url};\n概要：{summary};\n作者：{author};\n时间：{public_time};'
                DingTalks.compose(message)
            except Exception as e:

                conn.close()
                pass
        except Exception as w:
            pass


def ke_main():
    while True:
        try:

            KeInfo().get_36ke_venture_capital()

        except Exception as e:
            pass


if __name__ == '__main__':
    ke_main()
