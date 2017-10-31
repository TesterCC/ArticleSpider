#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/30 23:39'

# pip install selenium

from time import sleep

from selenium import webdriver

# 利用开源中国blog页面 用Selenium模拟鼠标下拉

# 设置chromedriver不加载图片（理由：不加载图片可以家加速chromedriver对整个页面的加载）
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)

browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_opt)     # 填写Chromedriver的路径, 如果已经将其加入环境变量，则要填"chromedriver"

# target_url = "https://www.oschina.net/blog"
target_url = "https://www.taobao.com"


browser.get(target_url)

sleep(5)

browser.quit()

print("Login Finish.")