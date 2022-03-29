# -*- coding: utf-8 -*-
import time
import re
import json
import requests
import smtplib
import hashlib
import psycopg2
import argparse
from selenium import webdriver
from requests import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions
from loguru import logger
from time import sleep
from lxml import etree
from fake_useragent import UserAgent as Ua

# 日志文件
logger.add("./Log/{time}_file.txt", rotation="00:00", retention='30 days', compression='zip', encoding='utf-8')

# 本地测试
# PG_SQL_LOCAL = {
#     'database': 'postgres',
#     'user': 'postgres',
#     'password': "123456",
#     # 'host':'10.27.78.1',
#     # 'host': 'localhost'
# }


# 服务器
PG_SQL_LOCAL = {
    'database': 'postgres',
    'user': 'pgadmin',
    'password': "dbc@2020",
    'host': '192.168.1.13',
    'port': '54321',
    'sslmode': 'disable',
    # 'TimeZone': 'Asia/Shanghai'
}


# 对标题添加指纹
@logger.catch  # 添加日志装饰器，自动记录代码异常处
def get_md5(url):
    # 将传入的字符串进行md5加密
    if isinstance(url, str):
        url = url.encode('utf-8')

    md5 = hashlib.md5()
    md5.update(url)
    return str(md5.hexdigest()).strip()


#  建表
@logger.catch  # 添加日志装饰器，自动将代码异常处记录
def new_pg():
    """建表  ----->已经建好，注释"""
    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()

    # id int not null primary key "主键" ,
    cursor.execute(
        """
        create table IF NOT EXISTS public.WeChat(
        id  serial PRIMARY KEY NOT NULL,
        area_id varchar(30) NOT NULL,
        crawledTime timestamp NOT NULL,
        news_type varchar(50) NOT NULL ,
        news_url varchar(255) NOT NULL ,
        news_title varchar(255) NOT NULL ,
        news_time varchar(20) NOT NULL ,
        news_author varchar(30) NOT NULL,
        news_content varchar NOT NULL,
        signature_md5 char(40) NOT NULL
        )"""
    )
    # area_id,crawledTime,news_type,news_url,news_title,news_time,news_author,news_content,title_cn,content_cn,is_read,remark,signature_md5,insert_time
    conn.commit()
    conn.close()


# pg数据库的增删改查
@logger.catch  # 添加日志装饰器，自动将代码异常处记录
def insert_into_pg(md5_figure, tuple_sql):
    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()

    # 查询
    cursor.execute("select signature_md5 from public.wechat")

    while True:
        md5_figures = cursor.fetchall()
        # print(md5_figures)
        if md5_figure in [str(md5_[0]).strip() for md5_ in list(set(md5_figures))]:
            break
        insert_sql = """
                    insert into public.WeChat(area_id,crawledTime,news_type,news_url,news_title,news_time,news_author,
                    news_content,signature_md5)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s) """

        # 执行 插入语句
        cursor.execute(insert_sql, tuple_sql)
        conn.commit()
        conn.close()
        break


# @logger.catch  # 添加日志装饰器，自动将代码异常处记录
def get_news_url(url, account_name):
    """
    selenium抓取公众号最新新闻链接
    """
    newsData = {}

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('headless')
    # chrome_options.add_argument(
    #     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    # chrome_options.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("lang=zh_CN.UTF-8")

    """ 实现规避检测 """
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 添加参数
    browser = webdriver.Chrome(chrome_options=chrome_options, options=option)

    browser.get(url)

    # 等待
    wait = WebDriverWait(browser, 5)
    key_input = wait.until(ec.presence_of_element_located((By.NAME, 'query')))
    key_input.send_keys(account_name)

    sleep(3)
    # 定位 点击位置并且点击
    browser.find_element_by_xpath('//input[@uigs="search_account"]').click()
    # try:

    #  等待直到出现了该元素
    print(browser.page_source)

    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'news-list2')))
    # WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.ID, "home")))

    # 定位该公众号的最新的一篇文章
    # 点击最新新闻并且进入到新标签，但是源码还停留在前标签
    # print(account_name)
    browser.find_element_by_xpath('//dd/a[contains(@uigs,"account_article")]').click()

    sleep(2)
    # 添加采集时间 、定义类型、公众号名称
    newsData['area_id'] = str(account_name)
    time_ = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    newsData['crawledTime'] = time_
    news_type = 'Public Accounts news'
    newsData['news_type'] = news_type

    """
    解析提取文章数据
    """
    handles = browser.window_handles  # 获取标签窗口数量
    browser.switch_to.window(handles[-1])  # 切换到最新的标签窗口即最后一个窗口

    print(browser.current_url)
    news_url = browser.current_url  # 获取selenium当前网页的链接，抛给requests去解析提取数据

    newsData['news_url'] = news_url
    sleep(2)
    browser.close()
    browser.quit()

    return news_url, newsData


# 采集数据的主函数
@logger.catch  # 添加日志装饰器，自动将代码异常处记录
def get_news_data(url, account_name):
    headers = {
        "authority": "mp.weixin.qq.com",
        "method": "GET",
        "path": "/s?src=11&timestamp=1603265618&ver=2657&signature=NJh25jTAXJHK8NDB-D1uWfDwQYsMbgA-KtGEZsJAAQ*XHqW4yIj2goyRuarp8eKs4tcoqk5HukEnxd-AynJLproT6hKnY3z1hMo1Xmo3yGIGBhFU-eY3iAPdtrM*Enn0&new=1",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "cookie": "RK=HlR4TdHTf6; ptcz=431558290bce0b8b208cd510d7a84c05b8156e6dc28d31f056ed602a72bd4b46; pgv_pvi=7456908288; eas_sid=01k5X873f4b9N1S9h9a8d9U495; pgv_pvid=7062000775; tvfe_boss_uuid=f7845b382b75eb76; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221745bebdca23d1-0c149ea1b1519b-4353760-1327104-1745bebdca38b9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221745bebdca23d1-0c149ea1b1519b-4353760-1327104-1745bebdca38b9%22%7D; _gcl_au=1.1.1490435895.1599793875; _ga=GA1.2.1234499412.1599793875; o_cookie=1364468984; pac_uid=1_1364468984; iip=0; ua_id=7acPBVmgN2lHzUnoAAAAAMbB_7Y8c5pnAeO4oIm5HnY=; openid2ticket_ojO_H5cw0-7LwZtfQtj-uiMdkac8=c6xS0SnrMKTqhC7MrjWTvwqruJ7rW3gx2RrpThrkWGA=; mm_lang=zh_CN; xid=a1f1eea981015e98940e4dc29e4428cb; _qpsvr_localtk=1603196267025; rewardsn=; wxtokenkey=777",
        "pragma": "no-cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
        # "user-agent": Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F,
        # "user-agent": Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36,
    }
    news_url, newsData = get_news_url(url, account_name)
    response = requests.get(news_url, headers=headers)
    response_ = str(response.text)
    if 200 <= response.status_code < 300:
        # area_id,crawledTime,news_type,news_url,news_title,news_time,news_author,news_content,title_cn,content_cn,is_read,remark,signature_md5,insert_time
        newsData['area_id'] = str(account_name)
        time_ = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        newsData['crawledTime'] = time_
        news_type = 'Public Accounts news'
        newsData['news_type'] = news_type

        html_codes = etree.HTML(response_)
        news_issue_title = ' '.join(html_codes.xpath('//h2[@id="activity-name"]//text()')).strip()
        # print('title:', news_issue_title)
        newsData['news_issue_title'] = news_issue_title
        news_issue_author = ','.join(
            html_codes.xpath('//span[@class="rich_media_meta rich_media_meta_text"]//text()')).strip()
        # print('author:', news_issue_author)
        newsData['news_issue_author'] = news_issue_author
        # 获取时间为网页的时间戳
        try:
            time_1 = re.compile('",n="(.*?)",s=', re.S).findall(str(response.text))
            news_time = int(' '.join(time_1))

            news_issue_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(news_time))
        except Exception:
            news_issue_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        # print('发布时间：', news_issue_time)
        newsData['news_issue_time'] = str(news_issue_time)

        # contents = html_codes.xpath('//div[@id="js_content"]/p|//div[@id="js_content"]/section')
        contents = html_codes.xpath('//div[@id="js_content"]//p|//div[@id="js_content"]/section/span')

        news_content_list = []
        for content_ in contents:
            test = content_.xpath('.//text()')
            if '相关链接' in str(test) or '如需转载' in str(test) or '查看系列文章' in str(test) or 'END' in str(
                    test) or '更多精彩内容，' in str(test):
                break
            if test == [] or test is None or test == ['']:
                pass
            news_content_list.append(''.join(test).strip())
        news_issue_content = "\n\n".join([c for c in news_content_list if c != ""]).strip()

        # print('内容：', news_issue_content)
        newsData['news_issue_content'] = news_issue_content

        title_cn = ''
        content_cn = ''
        is_read = ''
        remark = ''
        insert_time = ''
        # 建表
        new_pg()
        # 在增加数据前，需要查询有没有这一条数据即去重
        md5_figure = get_md5(str(news_issue_title))
        newsData['signature_md5'] = md5_figure
        # print(md5_figure)
        # 插入数据
        # area_id,crawledTime,news_type,news_url,news_title,news_time,news_author,news_content,title_cn,content_cn,
        # is_read,remark,signature_md5,insert_time
        # tuple_sql = (md5_figure, account_name, time_, news_type, news_url, news_issue_title, news_issue_time, news_issue_author,news_issue_content)
        tuple_sql = (account_name, time_, news_type, news_url, news_issue_title, news_issue_time, news_issue_author,
                     news_issue_content, md5_figure)
        insert_into_pg(md5_figure, tuple_sql)

        # 上服务器需要注释掉
        dumps_data = json.dumps(newsData, ensure_ascii=False)
        # with open('./newsData.json', 'a+', encoding='utf-8') as file:
        #     file.writelines(dumps_data)
        #     file.write('\n')
        #     file.close()
    else:
        logger.error('该网站异常！')


if __name__ == '__main__':
    while True:
        s_t = time.time()
        # 搜狗微信链接
        url = 'https://weixin.sogou.com/'
        public_account_name_list = ['国防科技要闻', '知远战略与防务研究所', '电科防务', '防务快讯', '天地一体化信息网络', '电科小氙']
        for public_account_name in list(set(public_account_name_list)):
            get_news_data(url, public_account_name)
        e_t = time.time()
        print('耗时：', e_t - s_t)
        sleep(60 * 30)
