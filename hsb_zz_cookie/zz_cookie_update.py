#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *
import pymysql
import datetime
import time
from loguru import logger

logger.add("./spiders/log/{time}.txt", encoding='utf-8')


@logger.catch
def update_zz_cookie_count():
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PASSWORD,
                           database=MYSQL_DATABASES)
    cursor = conn.cursor()
    update_sql = """UPDATE zz_cookie SET count_number = 0 where  count_number >2"""
    cursor.execute(update_sql)
    conn.commit()
    conn.close()
    logger.info(f'更新转转cookie计数')


while True:
    hour = datetime.datetime.now().hour
    if hour == 1:
        update_zz_cookie_count()
        time.sleep(60 * 60)
    else:
        time.sleep(60 * 10)
