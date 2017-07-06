# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

import MySQLdb

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"    # 把对象转换成json格式str
        self.file.write(lines)
        return item

    def spider_close(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json exporter导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 数据相关的存储自定义Pipeline完成
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'yanxi76543210', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    # 重载  记得对应items.py
    def process_item(self, item, spider):
        # insert_sql = """
        #     insert into jobbole_article(title, create_date, url, url_object_id, front_image_url, front_image_path, comment_nums, fav_nums, praise_nums, tags, content)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        # """
        # self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"], item["front_image_path"], item["comment_nums"], item["fav_nums"], item["praise_nums"], item["tags"], item["content"]))

        insert_sql = """
            insert into jobbole_article(title, create_date, url, comment_nums, fav_nums, praise_nums, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["comment_nums"], item["fav_nums"], item["praise_nums"], item["tags"]))

        self.conn.commit()

        # wait to test 4-14 07:09


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:          # result is tuple
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item