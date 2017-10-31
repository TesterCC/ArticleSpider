#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/30 23:39'

# pip install selenium

from time import sleep

from selenium import webdriver

# phantomjs, 无界面的浏览器，但多进程的情况下phantomjs的性能会严重下降
browser = webdriver.PhantomJS(executable_path="/Users/TesterCC/Development/phantomjs-2.1.1-macosx/bin/phantomjs")

target_url = "https://detail.tmall.com/item.htm?spm=a222t.8063993.4954155005.6.6209da3bxorZJa&acm=lb-zebra-164656-978614.1003.4.2269880&id=559791372740&scm=1003.4.lb-zebra-164656-978614.ITEM_559791372740_2269880&sku_properties=5919063:6536025;122216431:27772"

browser.get(target_url)

sleep(5)

print(browser.page_source)

browser.quit()

print("Login Finish.")