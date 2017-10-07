#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/6 21:26'

"""
for auto recognize zhihu Chinese captcha
"""

import requests
import shutil
import time
import re
import json

from zheye import zheye


z = zheye()

# Here is Mac Chrome User-Agent, if don't set, server will return 500
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

h = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    # "HOST": "www.zhihu.com",   # can use
    # "Referer": "https://www.zhihu.com/",
    "User-Agent": agent
}

lp = []
lpp = []

s = requests.session()
web_data = s.get('http://www.zhihu.com', headers=h).text

match_obj = re.match('.*name="_xsrf" value="(.*?)"', web_data, re.DOTALL)   # need to add flags
xsrf = ''
if match_obj:
    xsrf = match_obj.group(1)
randomNum = str(int(time.time()*1000))   # generate a random string
r = s.get("https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=cn".format(randomNum), headers=h, stream=True)

if r.status_code == 200:
    with open('pic_captcha.gif', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    positions = z.Recognize('pic_captcha.gif')
    print(positions)

# key code
captcha = {}
pos = positions
tmp = []
captcha['input_points'] = []
for poss in pos:
    tmp.append(float(format(poss[0]/2, '0.2f')))      # sample pic is 400*88, but zhihu pic is 200*44
    tmp.append(float(format(poss[1]/2, '0.2f')))
    captcha['input_points'].append(tmp)
    tmp = []


# Attention Security
username = input("Pleaes input username(phone):\n>>")     # only mobile phone，因为下面post_url访问的是phone_num登录入口
password = input("Pleaes input password:\n>>")

# print str(captcha)
params = {
    '_xsrf': xsrf,
    'password': password,
    # 未处理坐标顺序问题，故获取坐标时要注意
    'captcha': '{"img_size": [200, 44], "input_points": [[%.2f, %f],[%.2f, %f]]}' % (pos[0][1] / 2, pos[0][0] / 2, pos[1][1]/2, pos[1][0] / 2),
    # here: 1st is x axis, 2ed is y axis
    # 'captcha': str(captcha)
    'captcha_type': 'cn',
    'phone_num': username
}

print(params)

r = s.post('https://www.zhihu.com/login/phone_num', headers=h, params=params)

re_text = json.loads(r.text)
print(r.text)


