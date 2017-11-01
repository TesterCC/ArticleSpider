# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from time import sleep

from selenium import webdriver
from scrapy import signals
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from fake_useragent import UserAgent

from tools.crawl_xici_ip import GetIP


class ArticlespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    # 随机更换user-agent

    # receive crawler
    def __init__(self, crawler):
        # 用父类方法做初始化
        super(RandomUserAgentMiddleware, self).__init__()
        # self.user_agent_list = crawler.settings.get("user_agent_list", [])    # get settings->user_agent_list
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")     # get settings.py -> RANDOM_UA_TYPE, default is "random"

    # 参考pipelines.py中的from_settings的用法
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # 动态语言闭包特性，函数里面定义函数
        # 随机切换user-agent操作
        def get_ua():
            return getattr(self.ua, self.ua_type)

        # random_agent = get_ua()    # for Debug, can comment

        request.headers.setdefault('User-Agent', get_ua())


class RandomProxyMiddleware(object):

    """
    动态设置IP代理
    settings.py -> DOWNLOADER_MIDDLEWARES 配置后才会生效
    """
    def process_request(self, request, spider):
        get_ip = GetIP()   # 实例化
        request.meta["proxy"] = get_ip.get_random_ip()


# scrapy集成Selenium
class JSPageMiddleware(object):
    """
    通过Chrome请求动态网页
    settings.py -> DOWNLOADER_MIDDLEWARES 配置后才会生效
    """
    def process_request(self, request, spider):
        if spider.name == "jobbole5customloader":     # jobbole是class JobboleSpider中name
            # 实际开发中可能只是处理一部分url
            spider.browser.get(request.url)    # 如果spider中没有定义name，会抛异常
            sleep(3)
            print("访问:{0}".format(request.url))

            # 请求后不要转到downloader下载器
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)   # Default encoding is ascii

        # 使用Selenium模拟用户访问，实现未登录访问拉勾网
        if spider.name == "lagou_selenium":     # jobbole是class JobboleSpider中name
            # 实际开发中可能只是处理一部分url
            spider.browser.get(request.url)    # 如果spider中没有定义name，会抛异常
            sleep(4)    # 5s test passed
            print("访问:{0}".format(request.url))

            # 请求后不要转到downloader下载器
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)



