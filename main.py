#!/usr/bin/env python
# coding=utf-8

import sys
import os
from scrapy.cmdline import execute


# filepath = os.path.dirname(os.path.abspath(__file__))    ＃ 取文件路径的父目录
# print(filepath)   # /Users/TesterCC/Development/scrapy_workspace/ArticleSpider

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])    # run command in terminal "scrapy crawl jobbole"
# execute(["scrapy", "crawl", "jobbole2"])    # run command in terminal "scrapy crawl jobbole2"
# execute(["scrapy", "crawl", "jobbole3spider"])    # run command in terminal "scrapy crawl jobbole3spider"
execute(["scrapy", "crawl", "jobbole4loader"])    # run command in terminal "scrapy crawl jobbole4loader"