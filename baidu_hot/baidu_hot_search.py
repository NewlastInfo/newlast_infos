#!/usr/bin/env python
# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import time
import datetime
import asyncio
import aiohttp
import pymysql
from dingTalk_baidu_hot import DingTalks
from settings import *
from lxml import etree
from loguru import logger

# 日志文件
logger.add("./Log/{time}_file.txt", rotation="00:00", retention='30 days', compression='zip', encoding='utf-8')


class BaiDuHotSearch:
    # session = AioRequests()
    mysql_host = MYSQL_HOST
    mysql_user = MYSQL_USER
    mysql_port = MYSQL_PORT
    mysql_password = MYSQL_PASSWORD
    mysql_databases = MYSQL_DATABASES

    @logger.catch  # 添加日志装饰器，自动记录代码异常处
    @classmethod
    def get_req_params(cls):
        url = "https://top.baidu.com/board?tab=realtime"
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

    async def get_baidu_hot_search(self):
        req_params = self.get_req_params()
        async with aiohttp.ClientSession() as session:
            async with session.request(**req_params) as response:
                res_code = await response.text()
                html = etree.HTML(res_code)
                html_infos = html.xpath('//div[contains(@class,"QLoo h")]')
                # print(len(html_infos))
                for html_info in html_infos[:10]:
                    title = ''.join(html_info.xpath('.//div[contains(@class,"single-text")]//text()')).strip()
                    info_url = ''.join(html_info.xpath('.//a[contains(@class,"img-wrapper")]/@href')).strip()
                    summary = ''.join(html_info.xpath('.//div[contains(@class,"c_1m_jR l")]/text()')).strip()
                    hot_index = int(''.join(html_info.xpath('.//div[contains(@class,"hot-index")]/text()')).strip())
                    try:
                        ranking = int(''.join(html_info.xpath('.//div[contains(@class,"index_1Ew5p")]/text()')).strip())
                    except Exception as e:
                        ranking = 0
                    public_time = str(datetime.datetime.now().date())
                    # print(public_time)
                    tuple_sql = (title, info_url, summary, hot_index, ranking, public_time,)
                    await self.insert_baidu_hot_info_data(tuple_sql)
        time.sleep(3 * 60 * 60)

    async def insert_baidu_hot_info_data(self, tuple_sql: tuple):
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
                insert_sql = """insert into baidu_hot_info(title, info_url, summary, hot_index, ranking, public_time) values (%s,%s,%s,%s,%s,%s) """
                # 执行 存储语句
                cursor.execute(insert_sql, tuple_sql)
                conn.commit()
                conn.close()
                title, info_url, summary, hot_index, ranking, public_time = tuple_sql
                message = f'标题：{title};\n时间：{public_time};\n排名：{ranking};\n搜索指数：{hot_index};\n概要：{summary};\n链接：{info_url};'
                DingTalks.compose(message)
            except Exception as e:

                conn.close()
                pass
        except Exception as w:
            pass


def baidu_main():
    while True:
        try:
            loop = asyncio.get_event_loop()
            ke = BaiDuHotSearch().get_baidu_hot_search()
            loop.run_until_complete(ke)
        except Exception as e:
            pass


if __name__ == '__main__':
    baidu_main()
