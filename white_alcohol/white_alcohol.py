#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time
from selenium import webdriver
from lxml import etree
from selenium.webdriver.chrome.options import Options  # => 引入Chrome的配置
from dingTalk_white_alchol import DingTalks


class WhiteAlcohol:
    def __init__(self):
        self.url = "http://fund.eastmoney.com/161725.html"

    # 配置
    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    # 获取浏览器对象
    # driver = webdriver.Chrome(chrome_options=ch_options)
    ch_options.add_argument("--no-sandbox")  #
    driver = webdriver.Chrome(executable_path="/home/root/chromedriver", chrome_options=ch_options)

    def time_is_true(self):
        try:
            year = repr(datetime.datetime.now().year)
            month = repr(datetime.datetime.now().month)
            day = repr(datetime.datetime.now().day)
            hour = int(repr(datetime.datetime.now().hour))
            year_month_day = year + month + day

            week_what = int(datetime.datetime.strptime(year_month_day, "%Y%m%d").weekday() + 1)
            # if 0 < week_what < 6 and 8 <= hour <= 15:
            if 0 < week_what < 6:
                return True
            return False
        except Exception:
            return False

    def get_white_alcohol_code(self):
        time_is_true = self.time_is_true()
        if time_is_true:
            self.driver.get(self.url)
            time.sleep(10)
            html_code = etree.HTML(self.driver.page_source)
            phone_html_infos = html_code.xpath('//li[@id="position_shares"]//tbody/tr')
            try:
                for phone_html_info in phone_html_infos[1:]:
                    stock_name = ''.join(phone_html_info.xpath('./td[1]/a//text()')).strip()
                    proportion_rate = ''.join(phone_html_info.xpath('./td/text()')).strip()
                    high_low_rate = ''.join(phone_html_info.xpath('./td/span//text()')).strip()
                    # public_time = str(datetime.datetime.now().date())
                    # message = f'时间：{public_time};\n股票名称：{stock_name};\n占比：{proportion_rate};\n涨跌率：{high_low_rate};'
                    message = f'股票名称：{stock_name};\n股票占比：{proportion_rate};\n涨跌率  ：{high_low_rate};'
                    DingTalks.compose(message)
                    time.sleep(10)
            except Exception as e:
                print(e)
            time.sleep(60 * 30)
        else:
            time.sleep(60)


def return_white_alcohol():
    while True:
        try:
            white_alcohol = WhiteAlcohol()
            white_alcohol.get_white_alcohol_code()
        except Exception as e:
            print(f'error is {e}')


if __name__ == '__main__':
    return_white_alcohol()
