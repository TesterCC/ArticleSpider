#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'MFC'
__time__ = '18/2/10 22:40'


import re
import json
import datetime


try:
    import urlparse as parse
except:
    from urllib import parse

import scrapy
from scrapy.loader import ItemLoader
from items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = "zhihu_sel"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    #question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        """
        提取出html页面中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        # all_urls = response.css("a::attr(href)").extract()
        # all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # all_urls = filter(lambda x: True if x.startwith("https") else False, all_urls)
        # for url in all_urls:
        #     match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
        #     if match_obj:
        #         # 如果提取到question相关的页面，则下载后交由提取函数进行提取
        #         request_url = match_obj.group(1)
        #         yield scrapy.Request(request_url, headers=self.headers, callback=self.parse)
        #     else:
        #         # 如果不是question页面则直接进一步跟踪
        #         yield scrapy.Request(url, headers=self.headers, callback=self.parse)
        #         # 不写callback=XX也可以,回调默认会调parse()

        # 为了演示方便，上面注释
        pass

    def parse_question(self, response):
        # 处理question页面， 从页面中提取出具体的question item

        # 为了演示方便，上面注释，需要的参考zhihu.py
        pass

    def parse_answer(self, response):
        # 为了演示方便，上面注释，需要的参考zhihu.py
        pass

    def start_requests(self):

        # 原来的login()函数的逻辑直接代码写到start_requests()中， lagou也可以用这种方法登录
        from selenium import webdriver
        # browser = webdriver.Chrome(executable_path="E:/test/chromedriver.exe")

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        browser = webdriver.Chrome()
        # 某些高版本的mac os /usr/bin/没有复制权限，可以将driver复制到/usr/local/bin, path会优先去找这个路径, 在系统path中放了chromedriver就不用指定路径

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            "yourusername")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
            "yourzhihupassword")
        browser.find_element_by_css_selector(
            ".Button.SignFlow-submitButton").click()
        import time
        time.sleep(7)
        Cookies = browser.get_cookies()
        print(Cookies)
        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            # 写入文件
            # f = open('G:/scrapy/ArticleSpider/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
            f = open('/Users/TesterCC/Development/scrapy_workspace/ArticleSpider/ArticleSpider/cookies/' + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()

        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
