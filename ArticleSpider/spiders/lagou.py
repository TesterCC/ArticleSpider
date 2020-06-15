#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import os
import pickle
import scrapy


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import LagouJobItemLoader, LagouJobItem

from ArticleSpider.utils.common import get_md5
from settings import BASE_DIR

# switch ip when crawl lagou
class LagouSpider(CrawlSpider):        # 不能重写parse函数了，如果重写了parse其它功能就不能正常用了,重载要用这个函数parse_start_url
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    # start_urls = ['https://www.lagou.com/']     # most of websites use https
    start_urls = ['https://www.lagou.com/chengdu-zhaopin/go/']     # most of websites use https
    # start_urls = ['https://www.lagou.com/jobs/list_python']     # most of websites use https

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),        # 所有职位
        # Rule(LinkExtractor(allow=("jobs/.*",)), follow=True),        # 所有职位  2020
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),  # 公司页面的招聘信息
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

# 不使用   Attention: 既然用了CrawlSpider，那在爬虫开始之前就需要模拟登录，而是需要重载CrawlSpider的start_requests()
    # def parse_start_url(self, response):
    #     return []
    #
    # def process_results(self, response, results):
    #     return results

    def start_requests(self):
        # 去使用selenium模拟登录后拿到cookie交给scrapy的request使用
        # 1.通过Selenium模拟登录
        # 2.从文件中读取cookies
        cookies = []
        if os.path.exists(BASE_DIR+"/cookies/lagou.cookie"):
            cookies = pickle.load(open(BASE_DIR+"/cookies/lagou.cookie","rb"))

        if not cookies:

            from selenium import webdriver
            browser = webdriver.Chrome()   # 对应chromedriver我已经放到系统路径
            browser.get("https://passport.lagou.com/login/login.html")
            browser.find_element_by_xpath("/html/body/section/div[2]/div[1]/div[2]/form/div[1]/input").send_keys("13551856640")
            # browser.find_element_by_css_selector(".form_body .input input_white HtoC_JS").send_keys("13551856640")
            browser.find_element_by_css_selector('.form_body input[type="password"]').send_keys("-TesterCC07-")
            browser.find_element_by_css_selector('div[data-view="passwordLogin"] input.btn_lg').click()
            import time
            time.sleep(20)  # 留够时间，才能人工过验证码
            cookies = browser.get_cookies()
            # 写入cookie到文件中
            pickle.dump(cookies, open(BASE_DIR+"/cookies/lagou.cookie","wb"))   # 填相对路径, 如果有cookie就读取cookie登录

        # 要把cookie放入scrapy中，但是scrapy request使用cookie时不能直接使用
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]

        # 重写start_requests必要的逻辑
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, cookies=cookie_dict)

    def parse_job(self, response):
        # 解析拉勾网的职位

        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()

        # 尽量少写处理逻辑，关于数据的清洗放在ItemLoader函数中去做   css .class #id
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        # item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_xpath("title", "//div[@class='job-name']/@title")

        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))    # 参考jobbole4中的md5用法
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/h3/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/h3/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/h3/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/h3/span[5]/text()")
        item_loader.add_css("tags", ".position-label li::text")
        item_loader.add_css("publish_time", ".publish_time::text")     # need to convert str and split
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company a::attr(href)")
        item_loader.add_value("crawl_time", datetime.now())

        job_item = item_loader.load_item()
        return job_item
