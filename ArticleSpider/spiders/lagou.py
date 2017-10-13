#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import LagouJobItemLoader, LagouJobItem

from ArticleSpider.utils.common import get_md5


# switch ip when crawl lagou
class LagouSpider(CrawlSpider):        # 不能重写parse函数了,重载要用这个函数parse_start_url
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']     # most of websites use https

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),        # 所有职位
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),  # 公司页面的招聘信息
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

# 不使用
    # def parse_start_url(self, response):
    #     return []
    #
    # def process_results(self, response, results):
    #     return results

    def parse_job(self, response):
        # 解析拉勾网的职位

        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()

        # 尽量少写处理逻辑，关于数据的清洗放在ItemLoader函数中去做   css .class #id
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))    # 参考jobbole4中的md5用法
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")
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
