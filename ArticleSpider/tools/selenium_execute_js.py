#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/30 23:39'

# pip install selenium

from time import sleep

from selenium import webdriver

# 利用开源中国blog页面 用Selenium模拟鼠标下拉

browser = webdriver.Chrome(executable_path="chromedriver")     # 填写Chromedriver的路径, 如果已经将其加入环境变量，则要填"chromedriver"

target_url = "https://www.oschina.net/blog"

browser.get(target_url)

sleep(5)

# execute javascript code  --  Selenium 模拟鼠标下拉
# 模拟3次
for i in range(3):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")   # 网页正文全文高
    sleep(3)

browser.quit()

print("Login Finish.")