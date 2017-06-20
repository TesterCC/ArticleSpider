#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import re


# TARGET_URL = "http://blog.jobbole.com/108466/"
# 进入scrapy shell交互调试模式: scrapy shell http://blog.jobbole.com/108466/


class JobboleSpider(scrapy.Spider):
    name = "jobbole2"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/108466/']

    def parse(self, response):
        # use CSS Selector to locate Element
        # get title
        title = response.css(".entry-header h1::text").extract()      # CSS伪类选择器::

        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].replace("·", "").strip()      # 处理/r/n空格，处理点号，处理空格

        praise_nums = response.css(".vote-post-up h10::text").extract()[0]     # ' 2 收藏'

        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(r".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]    # ' 2 评论'
        match_re = re.match(r".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)

        content = response.css("div.entry").extract()[0]

        tags = response.css("p.entry-meta-hide-on-mobile::text").extract()[0]
        # 09:47

# --------------

        # get tag
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()    # ['开发', ' 2 评论 ', '数据科学', '机器学习']
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]     # ['开发', '数据科学', '机器学习']
        tags = ",".join(tag_list)      # '开发,数据科学,机器学习'
        pass