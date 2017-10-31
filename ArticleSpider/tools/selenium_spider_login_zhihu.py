#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/30 23:39'

# pip install selenium

from time import sleep

from selenium import webdriver
# from scrapy.selector import Selector

browser = webdriver.Chrome(executable_path="chromedriver")     # 填写Chromedriver的路径, 如果已经将其加入环境变量，则要填"chromedriver"
# chromedriver -h
# chromedriver --version

target_url = "https://www.zhihu.com/#signin"

zhihu_account = ""

zhihu_password = ""

browser.get(target_url)
# print(browser.page_source)

# click点击使用密码登录按钮
browser.find_element_by_css_selector(".signin-switch-password").click()

sleep(2)

# located inputbox username
# browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/form/div[1]/div[1]/input").send_keys(zhihu_account)
browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys(zhihu_account)

# located inputbox password
# browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/input").send_keys(zhihu_password)
browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys(zhihu_password)

# 这里要给输入验证码留足够的时间，或者看是否可以结合zheye库使用
sleep(10)

# click login button
browser.find_element_by_css_selector(".view-signin button.sign-button").click()

sleep(5)

browser.quit()