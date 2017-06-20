#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import re


# 进入scrapy shell交互调试模式: scrapy shell http://blog.jobbole.com/all-posts/
# Python分布式爬虫打造搜索引擎 Scrapy精讲 4-8 4-9 编写spider爬取jobbole的所有文章


class JobboleSpider(scrapy.Spider):
    name = "jobbole3spider"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']   # Get all article http://blog.jobbole.com/all-posts/

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy下载后进行解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse函数
        """
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        # http://blog.jobbole.com/all-posts/
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            print(post_url)
        # -- 4-8 10:30



        # use CSS Selector to locate Element
        # get title
        title = response.css(".entry-header h1::text").extract()[0]      # CSS伪类选择器::

        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].replace("·", "").strip()      # 处理/r/n空格，处理点号，处理空格

        praise_nums = response.css(".vote-post-up h10::text").extract()[0]     # ' 2 收藏'

        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(r".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]    # ' 2 评论'
        match_re = re.match(r".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)

        content = response.css("div.entry").extract()[0]

        # tag = response.css("p.entry-meta-hide-on-mobile a::text").extract()[0]    # '开发'
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()   # ['开发', ' 2 评论 ', '数据科学', '机器学习']

        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)     # '开发,数据科学,机器学习'

        pass