#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json
import time
import hmac
import base64
import hashlib
import requests
from urllib.parse import quote_plus


class DingTalks:
    access_token = 'dfaacd01d2c0cb95a4cc7ecd1dccf55f1d036db6b26f0783788de19d7420bf5c'
    webhook = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    secret = 'SEC4d44e711f7877e253f9468260eaad2ef20e6f1ad0d2b6441589c6f7b5fcbe815'

    headers = {'Content-Type': 'application/json'}

    @classmethod
    def compose(cls, content, msgtype='text'):
        url = cls.webhook
        if msgtype == 'text':
            msg = {
                "msgtype": msgtype,
                "text": {"content": content},
                "at": {"isAll": False},
            }
        else:
            msg = {
                "msgtype": msgtype,
                "markdown": {"title": "", "text": content},
                "at": {"atMobiles": [], "isAtAll": False}
            }
        req = dict(url=url + cls.sign(), headers=cls.headers, data=json.dumps(msg), method="POST")
        requests.request(**req)

    @classmethod
    def sign(cls):
        ts13 = repr(int(time.time() * 1000))
        str_to_en = f"{ts13}\n{cls.secret}"
        hmac_str = hmac.new(cls.secret.encode(), str_to_en.encode(), digestmod=hashlib.sha256).digest()
        hmac_str = quote_plus(base64.b64encode(hmac_str))
        suffix_url = f'&timestamp={ts13}&sign={hmac_str}'
        # print(suffix_url)
        return suffix_url


if __name__ == '__main__':
    DingTalks.compose("测试")
