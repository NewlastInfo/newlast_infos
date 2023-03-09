#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
from loguru import logger
from dingTalk_car import DingTalks
from lxml import etree


class CarInfo:

    @logger.catch  # 添加日志装饰器，自动将代码异常处记录
    def get_req_params(self, url):

        headers = {

            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",

        }
        req_params = dict(
            url=url,
            headers=headers,
        )
        return req_params

    def get_16888_car_add_rise(self):
        """
        汽车销量增幅排行榜
        """
        DingTalks.compose('******汽车销量增幅排行榜*************')
        url = "https://xl.16888.com/ranking-1.html"
        req_params = self.get_req_params(url)
        res_code = requests.get(url=req_params.get('url'), headers=req_params.get('headers')).text
        
        html = etree.HTML(res_code)
        html_infos = html.xpath('//table[@class="xl-table-def xl-table-a"]/tr')
        new_sell_count_name = ''
        old_sell_count_name = ''
        for html_info in html_infos[:1]:
            new_sell_count_name = ''.join(html_info.xpath('.//th[4]//text()')).strip()
            old_sell_count_name = ''.join(html_info.xpath('.//th[5]//text()')).strip()

        for html_info in html_infos[1:]:
            ranking = ''.join(html_info.xpath('.//td[1]//text()')).strip()
            product = ''.join(html_info.xpath('.//td[2]//text()')).strip()
            level = ''.join(html_info.xpath('.//td[3]//text()')).strip()
            new_sell_count = ''.join(html_info.xpath('.//td[4]//text()')).strip()
            old_sell_count = ''.join(html_info.xpath('.//td[5]//text()')).strip()
            rise_rate = ''.join(html_info.xpath('.//td[6]//text()')).strip()

            message = f'排名：{ranking};\n车型：{product};\n级别：{level};\n{new_sell_count_name}：{new_sell_count};\n{old_sell_count_name}：{old_sell_count};\n增长率：{rise_rate};'
            print(message)
            DingTalks.compose(message)

    def get_16888_car_reduce_rise(self):
        """
        汽车销量降幅排行榜

        """
        DingTalks.compose('******汽车销量降幅排行榜*************')
        url = "https://xl.16888.com/ranking-2.html"
        req_params = self.get_req_params(url)
        res_code = requests.get(url=req_params.get('url'), headers=req_params.get('headers')).text
        
        html = etree.HTML(res_code)
        html_infos = html.xpath('//table[@class="xl-table-def xl-table-a"]/tr')
        print(len(html_infos))
        new_sell_count_name = ''
        old_sell_count_name = ''
        for html_info in html_infos[:1]:
            new_sell_count_name = ''.join(html_info.xpath('.//th[4]//text()')).strip()
            old_sell_count_name = ''.join(html_info.xpath('.//th[5]//text()')).strip()

        for html_info in html_infos[1:]:
            ranking = ''.join(html_info.xpath('.//td[1]//text()')).strip()
            product = ''.join(html_info.xpath('.//td[2]//text()')).strip()
            level = ''.join(html_info.xpath('.//td[3]//text()')).strip()
            new_sell_count = ''.join(html_info.xpath('.//td[4]//text()')).strip()
            old_sell_count = ''.join(html_info.xpath('.//td[5]//text()')).strip()
            rise_rate = ''.join(html_info.xpath('.//td[6]//text()')).strip()

            message = f'排名：{ranking};\n车型：{product};\n级别：{level};\n{new_sell_count_name}：{new_sell_count};\n{old_sell_count_name}：{old_sell_count};\n增长率：{rise_rate};'
            print(message)
            DingTalks.compose(message)

    def get_16888_car_brand_ranking(self):
        """
        汽车品牌销量

        """
        DingTalks.compose('******汽车品牌销量*************')
        url = "https://xl.16888.com/brand.html"
        req_params = self.get_req_params(url)
        res_code = requests.get(url=req_params.get('url'), headers=req_params.get('headers')).text
        
        html = etree.HTML(res_code)
        html_infos = html.xpath('//table[@class="xl-table-def"]/tr')

        for html_info in html_infos[1:]:
            ranking = ''.join(html_info.xpath('.//td[1]//text()')).strip()
            brand = ''.join(html_info.xpath('.//td[3]//text()')).strip()
            country = ''.join(html_info.xpath('.//td[4]//text()')).strip()
            sell_count = ''.join(html_info.xpath('.//td[5]//text()')).strip()
            ratio = ''.join(html_info.xpath('.//td[6]//text()')).strip()

            message = f'排名：{ranking};\n品牌名称：{brand};\n国家：{country};\n销量：{sell_count};\n品牌份额：{ratio};'
            print(message)
            DingTalks.compose(message)

    def get_16888_car_product_selling_num(self):
        """
        车型销量
        """
        DingTalks.compose('******车型销量*************')
        url = "https://xl.16888.com/style.html"
        req_params = self.get_req_params(url)
        res_code = requests.get(url=req_params.get('url'), headers=req_params.get('headers')).text
        
        html = etree.HTML(res_code)
        html_infos = html.xpath('//table[@class="xl-table-def xl-table-a"]/tr')
        print(len(html_infos))

        for html_info in html_infos[1:]:
            ranking = ''.join(html_info.xpath('.//td[1]//text()')).strip()
            product = ''.join(html_info.xpath('.//td[2]//text()')).strip()
            sell_count = ''.join(html_info.xpath('.//td[4]//text()')).strip()
            company = ''.join(html_info.xpath('.//td[5]//text()')).strip()
            price = ''.join(html_info.xpath('.//td[6]//text()')).strip()
            message = f'排名：{ranking};\n车型：{product};\n销量：{sell_count};\n厂商：{company};\n价格：{price};'
            print(message)
            DingTalks.compose(message)

    def get_16888_car_e_product_selling_num(self):
        """
        电动车销量
        """
        DingTalks.compose('******电动车销量*************')
        url = "https://xl.16888.com/ev.html"
        req_params = self.get_req_params(url)
        res_code = requests.get(url=req_params.get('url'), headers=req_params.get('headers')).text
        
        html = etree.HTML(res_code)
        html_infos = html.xpath('//table[@class="xl-table-def xl-table-a"]/tr')
        print(len(html_infos))

        for html_info in html_infos[1:]:
            ranking = ''.join(html_info.xpath('.//td[1]//text()')).strip()
            product = ''.join(html_info.xpath('.//td[2]//text()')).strip()
            sell_count = ''.join(html_info.xpath('.//td[4]//text()')).strip()
            company = ''.join(html_info.xpath('.//td[5]//text()')).strip()
            price = ''.join(html_info.xpath('.//td[6]//text()')).strip()
            message = f'排名：{ranking};\n车型：{product};\n销量：{sell_count};\n厂商：{company};\n价格：{price};'
            print(message)
            DingTalks.compose(message)

    def get_16888_car_home_product_selling_num(self):
        """
        家用轿车销量
        """
        DingTalks.compose('******家用轿车销量*************')
        url = "https://xl.16888.com/car.html"
        req_params = self.get_req_params(url)
        res_code = requests.get(url=req_params.get('url'), headers=req_params.get('headers')).text
        
        html = etree.HTML(res_code)
        html_infos = html.xpath('//table[@class="xl-table-def xl-table-a"]/tr')
        print(len(html_infos))

        for html_info in html_infos[1:]:
            ranking = ''.join(html_info.xpath('.//td[1]//text()')).strip()
            product = ''.join(html_info.xpath('.//td[2]//text()')).strip()
            sell_count = ''.join(html_info.xpath('.//td[4]//text()')).strip()
            company = ''.join(html_info.xpath('.//td[5]//text()')).strip()
            price = ''.join(html_info.xpath('.//td[6]//text()')).strip()
            message = f'排名：{ranking};\n车型：{product};\n销量：{sell_count};\n厂商：{company};\n价格：{price};'
            print(message)
            DingTalks.compose(message)

    def get_16888_car_suv_product_selling_num(self):
        """
        SUV销量榜
        """
        DingTalks.compose('******SUV销量榜*************')
        url = "https://xl.16888.com/suv.html"
        req_params = self.get_req_params(url)
        res_code = requests.get(url=req_params.get('url'), headers=req_params.get('headers')).text
        
        html = etree.HTML(res_code)
        html_infos = html.xpath('//table[@class="xl-table-def xl-table-a"]/tr')
        print(len(html_infos))

        for html_info in html_infos[1:]:
            ranking = ''.join(html_info.xpath('.//td[1]//text()')).strip()
            product = ''.join(html_info.xpath('.//td[2]//text()')).strip()
            sell_count = ''.join(html_info.xpath('.//td[4]//text()')).strip()
            company = ''.join(html_info.xpath('.//td[5]//text()')).strip()
            price = ''.join(html_info.xpath('.//td[6]//text()')).strip()
            message = f'排名：{ranking};\n车型：{product};\n销量：{sell_count};\n厂商：{company};\n价格：{price};'
            print(message)
            DingTalks.compose(message)


def car_main():
    while True:
        try:
            CarInfo().get_16888_car_add_rise()
            CarInfo().get_16888_car_reduce_rise()
            CarInfo().get_16888_car_brand_ranking()
            CarInfo().get_16888_car_product_selling_num()
            CarInfo().get_16888_car_e_product_selling_num()
            CarInfo().get_16888_car_home_product_selling_num()
            CarInfo().get_16888_car_suv_product_selling_num()
        except Exception as e:
            print(e)
        time.sleep(60 * 60 * 18)


if __name__ == '__main__':
    car_main()
