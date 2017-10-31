#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/30 23:39'

# pip install selenium

from time import sleep

from selenium import webdriver

# Selenium完成微博模拟登录

browser = webdriver.Chrome(executable_path="chromedriver")     # 填写Chromedriver的路径, 如果已经将其加入环境变量，则要填"chromedriver"

target_url = "http://weibo.com/"

test_account = ""

test_password = ""

browser.get(target_url)

sleep(5)

browser.find_element_by_css_selector("#loginname").send_keys(test_account)
browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys(test_password)
browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

sleep(5)

browser.quit()

print("Login Finish.")