# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

import MySQLdb
import MySQLdb.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


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
    # 采用同步的机制写入mysql
    # 实例化时链接数据库
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
            insert into jobbole_article(title, url, create_date, fav_nums) 
            VALUES (%s, %s, %s, %s)
        """

        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"],  item["fav_nums"]))
        self.conn.commit()

        # this method is not good, because if crawler get much urls, insert speed is slower than craw speed, will cause data jamming.


# Mysql插入异步化
# Mysql config can write in settings.
class MysqlTwistedPipeline(object):
    # 采用异步的机制写入Mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 自定义组建和扩展时有用   Twisted只提供异步容器，调用还是用MySQL库
    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
            )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    # 重载  记得对应items.py
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)    # handle error

    # add self asynchronization handle error function
    def handle_error(self, failure):
        print(failure)    # 处理异步插入的异常

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item构建不同的sql语句并插入到mysql中
        # if item.__class__.__name__ == 'JobBoleArticleItem':   # 5-13 4:49
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums) 
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"],  item["fav_nums"]))


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # 增加容错性
        if "front_image_url" in item:
            for ok, value in results:          # result is tuple
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item