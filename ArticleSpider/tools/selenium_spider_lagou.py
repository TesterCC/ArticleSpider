#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/30 23:39'

# pip install selenium

from time import sleep

from selenium import webdriver
from scrapy.selector import Selector

driver = webdriver.Chrome(executable_path="chromedriver")     # 填写Chromedriver的路径, 如果已经将其加入环境变量，则要填"chromedriver"
# chromedriver -h
# chromedriver --version

# get taobao price
# target_url = "https://detail.tmall.com/item.htm?spm=a222t.8063993.4954155005.6.6209da3bxorZJa&acm=lb-zebra-164656-978614.1003.4.2269880&id=559791372740&scm=1003.4.lb-zebra-164656-978614.ITEM_559791372740_2269880&sku_properties=5919063:6536025;122216431:27772"
target_url = "https://www.lagou.com/"

driver.get(target_url)

sleep(2)

# click cd_btn  -- 但这个不好集成到操做中
driver.find_element_by_partial_link_text("成都").click()

sleep(2)

# t_selector = Selector(text=browser.page_source)
# print(t_selector.css(".tm-promo-price .tm-price::text").extract())   # 有促销价格的时候
# print(t_selector.css(".tm-price::text").extract())    # 无促销价格的时候

driver.quit()