#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItem(scrapy.Item):
    title = scrapy.Field()    # 统一Field()
    create_date = scrapy.Field()
    praise_nums = scrapy.Field()
    url = scrapy.Field()
    fav_nums = scrapy.Field()

