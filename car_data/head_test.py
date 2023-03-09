#!/usr/bin/env python
# -*- coding: utf-8 -*-

def header_dict(header_str):
    import re
    parttern = '(.*?):.(.*)'
    for line in header_str.splitlines():
        line = line.replace('"', '').replace('"', '')
        print(re.sub(parttern, r'"\1":"\2",', line))


if __name__ == '__main__':
    header_request = '''

accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7
cache-control: max-age=0
cookie: UM_distinctid=186b5d6bda39a0-0014a6ce80e9c7-26031951-1fa400-186b5d6bda6166; car16888_set_provinceId=6; car16888_set_cityId=77; car16888_set_area=2; car16888_set_areaName=%E6%B7%B1%E5%9C%B3; car16888_set_areaDir=sz; car16888_set_iscity=; CNZZDATA2314159=cnzz_eid%3D130302207-1678085994-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1678351361
sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36

'''
    header_dict(header_request)

