#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import hmac
import base64
import hashlib
import requests
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


if __name__ == '__main__':
    DingTalks.compose(msg="告警测试")
