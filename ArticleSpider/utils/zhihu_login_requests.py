#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

try:
    import cookielib    # 兼容Python2
except:
    import http.cookiejar as cookielib   # python 3 need import http.cookiejar


def zhihu_login(account, password):
    # Login Zhihu
    if re.match("^1\d{10}", account):   # 5-3 02:07
        print("")
# match moblie num,
# video match mobile num, here match e-mail [0-9a-zA-Z_]{0,19}@foxmail.com
# match all email address, ^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$





