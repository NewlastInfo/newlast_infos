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
    access_token = '1cb674952d43c106657f3b6b5f0de7d783339fee2050af56d69ea0fdc6c3d12c'
    webhook = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    secret = 'SEC7ee460b9e6ea71d2e9286aa06144ec24235ab8ea75585662eefd5f6163d56bb7'

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
