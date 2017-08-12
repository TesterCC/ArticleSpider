#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import Join


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


# nums可以通用
def get_nums(value):
    match_re = re.match(r".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    # 去掉tag中提取到的评论
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value

# 自定义Item loader，使字段只取第一个
class ArticleItemLoader(ItemLoader):
    # 自定义Item loader  -- jobbole5
    default_output_processor = TakeFirst()


# 运用自带Item loader
class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # input_processor=MapCompose(lambda x:x+"-jobbole")
        # input_processor=MapCompose(add_jobbole)
        # input_processor=MapCompose(lambda x: x+"-jobbole", add_jobbole)
    )    # 统一Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
        # output_processor=TakeFirst()    # 只取第一个   , jobbole5customloader no need.
    )

    url = scrapy.Field()    # url长度是变化的，用md5处理可以使URL变成唯一且长度固定的值 
    url_object_id = scrapy.Field()

    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value),   # return front_image_url原值，覆盖default_output_processor = TakeFirst()
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(","),
    )
    content = scrapy.Field()


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()


class ZhihuAnswerItem(scrapy.Item):
    # 知乎的问题回答 item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    creat_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

