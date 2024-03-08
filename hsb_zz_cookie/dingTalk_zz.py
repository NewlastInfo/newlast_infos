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


class ZzDingTalks:
    access_token = '93b7265cce9d9010e30fee238d7e6d0d992e337a4d7be2612812251ec1de0131'
    webhook = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    secret = 'SEC296066a6e0f10b5a235d43f0c8e1fb93bfbf24c168289cb83434e2e367754606'

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
                   'at': {
                       "atMobiles": [
                           18123771160,
                           15296003228,
                           15918718989,

                           # 也可以加入其他人
                       ],
                       'isAll': False
                   }
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


if __name__ == '__main__':
    ZzDingTalks.compose("测试")
