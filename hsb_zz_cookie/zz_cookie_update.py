#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *
import pymysql



def update_zz_cookie_count():
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PASSWORD,
                           database=MYSQL_DATABASES)
    cursor = conn.cursor()
    update_sql = """UPDATE zz_cookie SET count_number = 0 where  count_number >2"""
    cursor.execute(update_sql)
    conn.commit()
    conn.close()
