#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/108466/']

    def parse(self, response):
        # re_selector = response.xpath("/html/body/div[1]/div[3]/div[1]/div[1]/h1/text()")
        # re2_selector = response.xpath("//*[@id='post-108466']/div[1]/h1/text()")
        # re3_selector = response.xpath("//div[@class='entry-header']/h1/text()")
        # print(re3_selector.extract())      # 返回的中文文字乱码
        # print(re3_selector.extract()[0])

        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0]

        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·", "").strip()       # 处理/r/n空格，处理点号，处理空格

        praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]

        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(r".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(r".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)

        content = response.xpath("//div[@class='entry']").extract()[0]

        pass