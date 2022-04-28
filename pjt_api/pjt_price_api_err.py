#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import hmac
import time
import base64
import hashlib
import requests
import asyncio
from urllib.parse import quote_plus


class DingTalks:
    access_token = 'b6646c2071abc589658e8822ff304daa28100f498723297cb99a435c4fd091ea'
    webhook = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    secret = 'SECf2c1460dc4ca976bb1e02475510618319e69f896aba8413ac27b4d9fb7ee6b1c'

    @classmethod
    def sign(cls):
        ts13 = str(int(time.time() * 1000))
        str2en = '{}\n{}'.format(ts13, cls.secret)
        hmac_str = hmac.new(cls.secret.encode(), str2en.encode(), digestmod=hashlib.sha256).digest()
        hmac_str = quote_plus(base64.b64encode(hmac_str))
        return '&timestamp={}&sign={}'.format(ts13, hmac_str)

    @classmethod
    def compose(cls, content, msgtype='text'):
        url = cls.webhook
        if msgtype == 'text':
            msg = {'msgtype': msgtype,
                   'text': {'content': content},
                   'at': {'isAll': False}
                   }
        else:
            msg = {
                "msgtype": msgtype,
                "markdown": {"title": "", "text": content},
                "at": {"atMobiles": [], "isAtAll": False}
            }
        headers = {'Content-Type': 'application/json'}
        req = dict(url=url + cls.sign(), headers=headers, data=json.dumps(msg), method='POST')
        requests.request(**req)


class PriceApiErr(DingTalks):
    url = 'http://10.10.3.200:8000/docs#/'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "193.112.98.154:8000",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    }

    def return_ok(self):
        try:
            response = requests.get(url=self.url, headers=self.headers, timeout=3.8)
            if response.status_code == 200:
                return
            else:
                msg = f"爬价接口异常，请立即恢复"
                print(f"{msg}")
                self.compose(msg)
        except Exception:
            msg = f"爬价接口超时，请检查"
            print(f"{msg}")
            self.compose(msg)


def pjt_main():
    while True:
        try:
            price_api_err = PriceApiErr()
            price_api_err.return_ok()
            time.sleep(30 * 10)
        except Exception as e:
            time.sleep(30 * 10)


if __name__ == '__main__':
    pjt_main()
