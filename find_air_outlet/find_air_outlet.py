#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time
from selenium import webdriver
from lxml import etree
from selenium.webdriver.chrome.options import Options  # => 引入Chrome的配置
from dingTalk_find_air_outlet import DingTalks
from selenium.webdriver import ChromeOptions


class FindAirOutlet:
    def __init__(self):
        self.url = "https://data.eastmoney.com/bkzj/hy.html"

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
        # browser = webdriver.Chrome(chrome_options=chrome_options, options=option)
        return browser

    def time_is_true(self):
        try:
            year = repr(datetime.datetime.now().year)
            month = repr(datetime.datetime.now().month)
            day = repr(datetime.datetime.now().day)
            hour = int(repr(datetime.datetime.now().hour)) + 8
            # hour = int(repr(datetime.datetime.now().hour))
            year_month_day = year + month + day
            week_what = int(datetime.datetime.strptime(year_month_day, "%Y%m%d").weekday() + 1)
            if 0 < week_what < 6 and 9 <= hour <= 15:
                return True
            return False
        except Exception:
            return False

    def get_find_air_outlet_code(self):
        time_is_true = self.time_is_true()
        if time_is_true:
            browser = self.driver()
            browser.get(self.url)
            html_code = etree.HTML(browser.page_source)
            phone_html_infos = html_code.xpath('//div[@class="dataview-body"]//tbody/tr')
            try:
                for phone_html_info in phone_html_infos[:3]:  # 只取前3个风口行业
                    industry_sort_num = ''.join(phone_html_info.xpath('./td[1]//text()')).strip()
                    industry_name = ''.join(phone_html_info.xpath('./td[2]/a//text()')).strip()
                    high_low_rate = ''.join(phone_html_info.xpath('./td[4]/span//text()')).strip()
                    # 主力流入净额
                    Net_inflow_of_main_forces_num = ''.join(phone_html_info.xpath('./td[5]/span//text()')).strip()
                    # 主力流入净额比率
                    Net_inflow_of_main_forces_rate = ''.join(phone_html_info.xpath('./td[6]/span//text()')).strip()

                    # 今日超大单净流入净额
                    Today_super_large_single_net_inflow_num = ''.join(
                        phone_html_info.xpath('./td[7]/span//text()')).strip()
                    # 今日超大单净流入比率
                    Today_super_large_single_net_inflow_rate = ''.join(
                        phone_html_info.xpath('./td[8]/span//text()')).strip()

                    # 今日大单净流入净额
                    Net_inflow_of_large_orders_today_num = ''.join(
                        phone_html_info.xpath('./td[9]/span//text()')).strip()
                    # 今日大单净流入比率
                    Net_inflow_of_large_orders_today_rate = ''.join(
                        phone_html_info.xpath('./td[10]/span//text()')).strip()

                    # 今日中单净流入净额
                    Net_inflow_of_middle_order_today_num = ''.join(
                        phone_html_info.xpath('./td[11]/span//text()')).strip()
                    # 今日中单净流入比率
                    Net_inflow_of_middle_order_today_rate = ''.join(
                        phone_html_info.xpath('./td[12]/span//text()')).strip()

                    # 今日小单净流入净额
                    Net_inflow_of_small_order_today_num = ''.join(
                        phone_html_info.xpath('./td[13]/span//text()')).strip()
                    # 今日小单净流入比率
                    Net_inflow_of_small_order_today_rate = ''.join(
                        phone_html_info.xpath('./td[14]/span//text()')).strip()

                    # 今日主力净流入最大股名称
                    The_largest_net_inflow_of_major_stocks_today_name = ''.join(
                        phone_html_info.xpath('./td[15]/a//text()')).strip()

                    # public_time = str(datetime.datetime.now().date())
                    hour = int(repr(datetime.datetime.now().hour)) + 8
                    message = f'找风口的时间：{hour}时;' \
 \
                              f'\n风口行业顺序：{industry_sort_num};' \
 \
                              f'\n风口行业名称：{industry_name};' \
 \
                              f'\n涨跌率：{high_low_rate};' \
 \
                              f'\n主力流入净额：{Net_inflow_of_main_forces_num};' \
 \
                              f'\n主力流入净额比率：{Net_inflow_of_main_forces_rate};' \
 \
                              f'\n今日超大单净流入净额：{Today_super_large_single_net_inflow_num};\n今日超大单净流入比率：{Today_super_large_single_net_inflow_rate};' \
 \
                              f'\n今日大单净流入净额：{Net_inflow_of_large_orders_today_num};\n今日大单净流入比率：{Net_inflow_of_large_orders_today_rate};' \
 \
                              f'\n今日中单净流入净额：{Net_inflow_of_middle_order_today_num};\n今日中单净流入比率：{Net_inflow_of_middle_order_today_rate};' \
 \
                              f'\n今日小单净流入净额：{Net_inflow_of_small_order_today_num};\n今日小单净流入比率：{Net_inflow_of_small_order_today_rate};' \
 \
                              f'\n今日主力净流入最大股名称：{The_largest_net_inflow_of_major_stocks_today_name};'
                    DingTalks.compose(message)
                DingTalks.compose('间隔')

            except Exception as e:
                print(e)
            time.sleep(60 * 30)
        else:
            time.sleep(60)


def return_data():
    while True:
        try:
            find_air_outlet = FindAirOutlet()
            # find_air_outlet.get_find_air_outlet_code()
            print(8888888)
            time.sleep(100)
        except Exception as e:
            print(f'error is {e}')


if __name__ == '__main__':
    return_data()
