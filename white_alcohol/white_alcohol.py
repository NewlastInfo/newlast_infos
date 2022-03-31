#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time
from selenium import webdriver
from lxml import etree
from selenium.webdriver.chrome.options import Options  # => 引入Chrome的配置
from dingTalk_white_alchol import DingTalks
from selenium.webdriver import ChromeOptions


class WhiteAlcohol:
    def __init__(self):
        self.url = "http://fund.eastmoney.com/161725.html"

    def driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('log-level=3')
        chrome_options.add_argument('headless')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("lang=zh_CN.UTF-8")

        """ 实现规避检测 """
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 添加参数
        browser = webdriver.Chrome(executable_path="/home/root/chromedriver", chrome_options=chrome_options,
                                   options=option)
        return browser

    def time_is_true(self):
        try:
            year = repr(datetime.datetime.now().year)
            month = repr(datetime.datetime.now().month)
            day = repr(datetime.datetime.now().day)
            hour = int(repr(datetime.datetime.now().hour)) + 8
            year_month_day = year + month + day
            week_what = int(datetime.datetime.strptime(year_month_day, "%Y%m%d").weekday() + 1)
            if 0 < week_what < 6 and 9 <= hour <= 15:
                # if 0 < week_what < 6:
                return True
            return False
        except Exception:
            return False

    def get_white_alcohol_code(self):
        time_is_true = self.time_is_true()
        if time_is_true:
            browser = self.driver()
            browser.get(self.url)
            html_code = etree.HTML(browser.page_source)
            phone_html_infos = html_code.xpath('//li[@id="position_shares"]//tbody/tr')
            try:
                for phone_html_info in phone_html_infos[1:]:
                    stock_name = ''.join(phone_html_info.xpath('./td[1]/a//text()')).strip()
                    proportion_rate = ''.join(phone_html_info.xpath('./td/text()')).strip()
                    high_low_rate = ''.join(phone_html_info.xpath('./td/span//text()')).strip()
                    # public_time = str(datetime.datetime.now().date())
                    hour = int(repr(datetime.datetime.now().hour)) + 8
                    message = f'股票时间：{hour};\n股票名称：{stock_name};\n占比：{proportion_rate};\n涨跌率：{high_low_rate};'
                    # message = f'股票名称：{stock_name};\n股票占比：{proportion_rate};\n涨跌率  ：{high_low_rate};'
                    DingTalks.compose(message)
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
