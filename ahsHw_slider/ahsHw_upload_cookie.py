#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import redis

ahsHw_cookie_name = "token:accounts:ahsHw_cookie"

# prod_r = redis.Redis(host='spider200', password='d2hvYW1pOmlhbXdobw==', db=6, decode_responses=True)
prod_r = redis.Redis(host='193.112.98.154', password='d2hvYW1pOmlhbXdobw==', db=6, decode_responses=True)

cookies = """






acw_tc=76b20ff116608684683903642e5f1d805759ad98a9bc0c970f331d64e40799; sajssdk_2015_cross_new_user=1; _uab_collina=166086846850071283181692; USER_SESSION_ID_V3=a0f02e99-8432-4ab6-9551-0e91b47b2a7b; ssxmod_itna2=QqmOY5GK3HDKGHoiQ0o0ILqGu6N1UIKGYtUD8qZ4BKD/zDFxAIO9BevhdB7GFKeMa+sxvm0cjsytS3Y07wC/TgKHT/rm5FAkEKu3H44X/kld5Iov95FnV0b03kjqIgR5hkgXeZRZlGq5lzSQ4Pnf9+o=EG43mCedD5qfeo3i4BrrPgh628RuAi3nHB+Abu4QHAlKL7acvDoKzzSDaXC4jj3FybS5k6bE9ncpZjZp=/EXMKrg7tBfvt1a3o484eFo8EnAHiYaLbYAni8KjbqSdKvjFFWaFSd=z7O1A=vbTKwD4IDSuvPNsSOiu5ouYtYGvxG/G4rxdTDiuAN7GQ/GPQ47Bg+27samPehsaQqCj3B2KmQ3e0mxrNq+hodTaCxCnYTDNgGInGi3hDEgPDgTodr7uNajvEj+TGoZf=FL+5d3qDN9fNiSK3gvoLmFe5ffGuSO8mKSlLeEos1LH6+ok8CpYFfLq1qW8+9h5B8QEuQE23odNHcP/1DTuFDrArLYous4kIQLNDO+YWEPgKkr0sRIo7NupwhEiwOdnrAADDw=xZARxmKj2Rd7LTu+W5vOn8k1GMASA04pnNncTvl015pqBuODGcDG7tiDD===; ssxmod_itna=YqRxcD0D270QD=DkDzZWTaQ+DBeZqYDy7i1ED05ueGzDAxn40iDt=xV0hQPtm0o4a+K7Cexpv5fQ+ShxpYi6M2eDHxY=DUc7DIUD4+KGwD0eG+DD4DWDmWFDnxAQDjxGPnUpNH=DEDm48DWPDYxDrAoKDRxi7DDvdHx07DQ58rnD4AaBaoKHmXcih3AD8D7ymDlpxAIOwEU34ya7AwS53+x0kB40OuP5zOPoDUjFzng5N3=DaMQD5T7G3=AD5elD4=exaFADH+A=4MiZqe0xIhkRe+LUDD==; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22182b3799e7a344-0b399e6aa1d2cb-45647f52-1327104-182b3799e7bd61%22%2C%22%24device_id%22%3A%22182b3799e7a344-0b399e6aa1d2cb-45647f52-1327104-182b3799e7bd61%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D





"""


# USER_SESSION_ID_V3 = ''.join(re.compile(r'USER_SESSION_ID_V3=(.*?); ').findall(cookies)).strip()
USER_SESSION_ID_V3 = cookies.strip()
# USER_SESSION_ID_V3 = ''.join(re.compile(r'USER_SESSION_ID_V3=(.*?) ').findall(cookies)).strip()
print(USER_SESSION_ID_V3)

a = prod_r.hdel(ahsHw_cookie_name, "ahsHw_cookie")
v = prod_r.hset(ahsHw_cookie_name, "ahsHw_cookie", USER_SESSION_ID_V3)
# USER_SESSION_ID_V3 = prod_r.hget(ahsHw_cookie_name,'ahsHw_cookie')
# print(USER_SESSION_ID_V3)

