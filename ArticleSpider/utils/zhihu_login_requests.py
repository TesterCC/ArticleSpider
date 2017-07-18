#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

try:
    import cookielib    # 兼容Python2
except:
    import http.cookiejar as cookielib   # python 3 need import http.cookiejar


# match moblie num, ^1\d{10}
# video match mobile num, here match e-mail [0-9a-zA-Z_]{0,19}@foxmail.com
# match all email address, ^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$


def zhihu_login(account, password):
    # Login Zhihu
    # if re.match("^1\d{10}", account):
    if re.match("^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$", account):   # match e-mail
        print("邮箱登陆")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": "",
            "phone_num": account,
            "password": password
        }







