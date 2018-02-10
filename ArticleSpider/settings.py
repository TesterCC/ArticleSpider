#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


# Scrapy settings for ArticleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ArticleSpider'

SPIDER_MODULES = ['ArticleSpider.spiders']
NEWSPIDER_MODULE = 'ArticleSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ArticleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'ArticleSpider.middlewares.JSPageMiddleware': 1,    # 动态网页爬取才需要，比如用Selenium爬取
   # 'ArticleSpider.middlewares.RandomUserAgentMiddleware': 543,
   # 'ArticleSpider.middlewares.RandomProxyMiddleware': 542,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
   #  'ArticleSpider.pipelines.JsonWithEncodingPipeline': 2,
   #  'ArticleSpider.pipelines.JsonExporterPipeline': 3,
   # 'scrapy.pipelines.images.ImagesPipeline': 1,
   #  'ArticleSpider.pipelines.ArticleImagePipeline': 1,
   #  'ArticleSpider.pipelines.MysqlPipeline': 1,
    'ArticleSpider.pipelines.MysqlTwistedPipeline': 1,
}

project_dir = os.path.abspath(os.path.dirname(__file__))

IMAGES_URLS_FIELD = 'front_image_url'     # 传到pipeline时将这个值当数组处理
IMAGES_STORE = os.path.join(project_dir, 'images')
# print(">>>>>>>>>>>>>>>>>"+IMAGES_STORE)

# 设置ArticleSpider为Sources Root
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# print(BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'ArticleSpider'))
# sys.path.insert(0, "/Users/TesterCC/Development/scrapy_workspace/ArticleSpider/ArticleSpider")

# download pictures must bigger 100x100
# IMAGES_MIN_HEIGHT = 100
# IMAGES_MIN_WIDTH = 100


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MySQL config
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'article_spider'
MYSQL_USER = 'root'
MYSQL_PASSWORD = "yanxi76543210"

# SQL date format config
SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"

# User Agent Config
# USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:55.0) Gecko/20100101 Firefox/55.0"

# user_agent_list = [
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:55.0) Gecko/20100101 Firefox/55.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
# ]

RANDOM_UA_TYPE = "random"
