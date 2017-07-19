#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

try:
    import cookielib    # 兼容Python2
except:
    import http.cookiejar as cookielib   # python 3 need import http.cookiejar


session = requests.session()   # 用session获取, 代表某一次链接
# Set header use User-Agent
# Here is mobile User-Agent
agent = "User-Agent:Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    'User-Agent': agent
}


def get_xsrf():
    # get xsrf code
    # Because default User-Agent is Python2/Python3 , so zhihu will return 500 erorr. Anti crawler method.
    # response = requests.get("https://www.zhihu.com", headers=header)     # headers can custom
    response = session.get("https://www.zhihu.com", headers=header)     # more effective

    # print(response.text)

    # text = '<input type="hidden" name="_xsrf" value="f475b46b989c43c21162781cdc76a477"/>'

    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        # print(match_obj.group(1))
        return (match_obj.group(1))
    else:
        return ""


# match moblie num, ^1\d{10}
# video match mobile num, here match e-mail [0-9a-zA-Z_]{0,19}@foxmail.com
# match all email address, ^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$


def zhihu_login(account, password):
    # Login Zhihu
    # if re.match("^1\d{10}", account):
    if re.match("^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$", account):   # match e-mail
        print("邮箱登陆")
        # post_url = "https://www.zhihu.com/login/phone_num"   # video url
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password
        }

    # create post request
        response_text = session.post(post_url, data=post_data, headers=header)

        session.cookies.save()


if __name__ == '__main__':
    # get_xsrf()
    zhihu_login("testerlyx@foxmail.com", "-TesterCC07-")



