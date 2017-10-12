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

from settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT
from utils.common import extract_num

from w3lib.html import remove_tags      # for remove tags


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

    def get_insert_sql(self):
        insert_sql = """
                    insert into jobbole_article(title, url, create_date, fav_nums) 
                    VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title), fav_nums=VALUES(fav_nums)
                """
        params = (self["title"], self["url"], self["create_date"], self["fav_nums"])
        return insert_sql, params


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
                    insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num, 
                    watch_user_num, click_num, crawl_time) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
                    watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num), crawl_time=VALUES(crawl_time)
        """

        zhihu_id = self["zhihu_id"][0]  # the other way -- int("".join(self["zhihu_id"])) 转int，因为在数据库中是int类型 这里不用是因为zhihu.py中已经处理过
        topics = ",".join(self["topics"])
        url = self["url"][0]         # "".join(self["zhihu_id"])
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))
        # watch_user_num = extract_num("".join(self["watch_user_num"]))
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)     # strftime 将time转化为时间类型

        # 处理click_num的问题
        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0

        # 和insert into中的各个值顺序保持一致
        params = (zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎的问题回答 item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
                    insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, comments_num, 
                    create_time, update_time, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE content=VALUES(content), praise_num=VALUES(praise_num), comments_num=VALUES(comments_num),
                    update_time=VALUES(update_time)
        """

        # 因为json的两个time从json中传递过来时是int类型，所以要对create_time  update_time做单独处理,将int型转换为datetime型
        create_time = datetime.datetime.fromtimestamp(self["create_time"])
        update_time = datetime.datetime.fromtimestamp(self["update_time"])

        # 因为提取answer代码处是提取具体字段，不再是数组，可以直接返回
        params = (
            self["zhihu_id"], self["url"], self["question_id"], self["author_id"], self["content"],
            self["praise_num"], self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params


# About lagou spider
def remove_slash(value):
    # 去掉工作城市的斜线
    return value.replace("/", "")


class LagouJobItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息
    # 参考数据库字段
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_slash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_slash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_slash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags),
    )
    job_addr = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(","),
    )
    crawl_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )

