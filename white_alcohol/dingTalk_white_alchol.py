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
    access_token = '50f1c026bbfe4f27ccff203f6d9cf7b4a7ed7ec0593202a9d07f9f82097d4f43'
    webhook = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    secret = 'SEC0b2582568b3e082befe5e4555ce79f225dc3cf453ecb41fc159a97b3fffb2d6d'

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
