#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/11/1 18:06'


from time import sleep

from selenium import webdriver
from pyvirtualdisplay import Display

# pip install pyvirtualdisplay

# chrome无界面运行  - linux下可行，windows好像不行, mac下好像也不行

display = Display(visible=False, size=(800, 600))    # visible False , don't display
display.start()

browser = webdriver.Chrome(executable_path="chromedriver")     # 填写Chromedriver的路径, 如果已经将其加入环境变量，则要填"chromedriver"

target_url = "https://www.lagou.com/zhaopin/"

browser.get(target_url)

print(browser.current_url)
print(browser.title)

browser.quit()