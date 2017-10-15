#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/16 02:05'

"""
获取高匿代理
http://www.xicidaili.com/nn/
"""
from time import sleep

import requests
import MySQLdb
from scrapy.selector import Selector
from fake_useragent import UserAgent


conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='yanxi76543210', db='article_spider', charset="utf8")
cursor = conn.cursor()


# 也可以用scrapy写，但是太麻烦了。
def crawl_ips():
    # 爬去西刺的免费ip代理 这里也封ip的
    # headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:55.0) Gecko/20100101 Firefox/55.0"}    #  可以用list，也可以用fake－useragent

    ua = UserAgent()
    headers = {"User-Agent": ua.random}  # 保险一点，这里headers也随机获取

    for i in range(500):    # 2450是xici的代理页数，以后肯定还会持续增加
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        # print(re.text)   # for Debug
        sleep(3)   # 以防被block，xici封的应该是IP

        # 用scrapy的selector提取数据
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")

        ip_list = []

        for tr in all_trs[1:]:       # 防止第一行tr被取到
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]
            # print(all_texts)   ＃ for Debug

            ip_list.append((ip, port, speed, proxy_type))

        # 把取到的每一页的ip_list信息存入到数据库中   SQL字符串用法中插入字符varchar要传入单引号
        for ip_info in ip_list:
            cursor.execute(
                "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}','{1}',{2},'{3}') ON DUPLICATE KEY UPDATE port=VALUES(port), speed=VALUES(speed), proxy_type=VALUES(proxy_type)".format(
                    ip_info[0], ip_info[1], ip_info[2], ip_info[3]
                )
            )

            # 将SQL语句提交到数据库中
            conn.commit()      # commit是conn的用法


class GetIP(object):

    def delete_ip(self, ip):
        # 从数据库中删除无效的IP
        delete_sql = """
                     DELETE FROM proxy_ip WHERE ip='{0}' 
                     """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)

        try:
            proxy_dict = {
                "http": proxy_url
                # "https": proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
            code = response.status_code
            if 200 <= code < 300:
                print("Effective IP.")
                return True
            else:
                print("Invalid IP or Port")
                self.delete_ip(ip)
                return False
        except Exception as e:
            print("Invalid IP or Port.")
            self.delete_ip(ip)
            return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = """
                     SELECT ip, port FROM proxy_ip ORDER BY RAND() LIMIT 1
                     """
        result = cursor.execute(random_sql)

        for ip_info in cursor.fetchall():     # 接收全部的返回结果行
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                print("Judge Failed, to next one.")
                return self.get_random_ip()


if __name__ == '__main__':
    get_ip = GetIP()
    get_ip.get_random_ip()     
    # print(crawl_ips())  for debug

