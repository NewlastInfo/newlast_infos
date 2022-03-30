#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import json
import datetime
import time
from dingTalk_dh import DingTalks
from collections import Counter  # 引入Counter
from loguru import logger


class DhName2id:
    list_name = "map:dh:name2id"

    @logger.catch  # 添加日志装饰器，自动将代码异常处记录
    def get_true_or_false(self):
        prod_r = redis.Redis(host='193.112.98.154', password='d2hvYW1pOmlhbXdobw==', db=6, decode_responses=True)

        data_dh_dict = prod_r.hgetall(self.list_name)
        value_list = []
        key_list = []
        for key, values in data_dh_dict.items():
            value_list.append(int(values))
            key_list.append(key)

        value_list = sorted(value_list, reverse=False)
        value_non_list = sorted(list(set(value_list)), reverse=False)

        # print(len(value_list))
        # print('name2id映射去重后的值的数量', len(value_non_list))

        value_list = dict(Counter(value_list))
        dh_repeat_value = {key: value for key, value in value_list.items() if value > 1}  # 展现重复元素和重复次数
        for key, value in dh_repeat_value:
            message = repr(key)
            DingTalks.compose(f'当换有重复id值，请立即检查\n 重复值为{message}')
        time.sleep(30 * 60)


def return_dh_name2id():
    while True:
        try:
            dh_name2id = DhName2id()
            dh_name2id.get_true_or_false()
        except Exception as e:
            print(f'error is {e}')


if __name__ == '__main__':
    return_dh_name2id()
