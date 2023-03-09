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

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Cookie: qgqp_b_id=28aa01099e9d10abb71f87046fc41705; st_si=16726273495621; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; fund_trade_trackid=A9HQ/orsh0KHIDj0A6I6MFuZTovw5yOhjRwRDweccO4jT15I561PxnTVH39wxuzAe4XNk7jnib7uPWaccgjsoQ==; LToken=a89b0ea7d0fd44d28fcbe8a0ab09fb5c; st_asi=delete; st_pvi=74497741461518; st_sp=2022-09-05%2015%3A17%3A59; st_inirUrl=https%3A%2F%2Fwww.hao123.com%2Flink%2Fhttps%2F; st_sn=749; st_psi=20230309163942967-113300300820-5558731879
Host: data.eastmoney.com
sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36
'''
    header_dict(header_request)

