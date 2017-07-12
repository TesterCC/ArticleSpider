#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 将title取到的实际值传到value里面
def add_jobbole(value):
    return value + "-lily"


# 将create_date取到的实际值传到value里面
def date_convert(value):
    # need to convert create_date str to date class
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


# 自定义Item loader，使字段只取第一个
# class ArticleItemLoader(ItemLoader):
# 4-17 5:05

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # input_processor=MapCompose(lambda x:x+"-jobbole")
        # input_processor=MapCompose(add_jobbole)
        input_processor=MapCompose(lambda x: x+"-jobbole", add_jobbole)
    )    # 统一Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()    # 只取第一个
    )

    url = scrapy.Field()    # url长度是变化的，用md5处理可以使URL变成唯一且长度固定的值 
    url_object_id = scrapy.Field()

    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

