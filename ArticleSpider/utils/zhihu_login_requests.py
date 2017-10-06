#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
just for solve zhihu login issue, manual input captcha
"""

import re
import requests
import time

try:
    import cookielib    # 兼容Python2
except:
    import http.cookiejar as cookielib   # python 3 need import http.cookiejar


session = requests.session()   # 用session获取, 代表某一次链接
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")    # LWP实例化的cookie可直接调用save方法
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie未能加载")


# Set header use User-Agent
# Here is mobile User-Agent
agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36"
# agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": agent
}


def is_login():
    # 通过个人中心页面返回状态码来判断是否为登陆状态
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)     # allow_redirects default is True
    if response.status_code != 200:    # if login success , it will return 200 OK, if return 302, it means login failed.
        # return False
        return "Login Failed."
    else:
        # return True
        return "Login Success."


def get_xsrf():
    # get xsrf code
    # Because default User-Agent is Python2/Python3 , so zhihu will return 500 erorr. Anti crawler method.
    # response = requests.get("https://www.zhihu.com", headers=header)     # headers can custom
    response = session.get("https://www.zhihu.com", headers=header)     # more effective

    # print(response.text)

    # text = '<input type="hidden" name="_xsrf" value="f475b46b989c43c21162781cdc76a477"/>'

    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)   # need to add flags
    if match_obj:
        # print(match_obj.group(1))
        return match_obj.group(1)
    else:
        return "Match failed."


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("OK")


def get_captcha():
    # https://www.zhihu.com/captcha.gif?r=1492648311082&type=login&lang=en   英文验证码四位字母
    # https://www.zhihu.com/captcha.gif?r=1492648311082&type=login&lang=cn   倒立汉字
    import time
    t = str(int(time.time()*1000))     # 默认情况下python的时间戳是以秒为单位输出的float,通过把秒转换毫秒的方法获得13位的Unix时间戳
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=en".format(t)
    print(captcha_url)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg", "wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        return "Image Handle Error."

    captcha = input("请输入英文字母验证码\n>>")
    return captcha


# match moblie num, ^1\d{10}
# video match mobile num, here match e-mail [0-9a-zA-Z_]{0,19}@foxmail.com
# match all email address, ^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$
def zhihu_login(account, password):
    # Login Zhihu
    if re.match("^1\d{10}", account):
        print("手机号码登陆")
        post_url = "https://www.zhihu.com/login/phone_num"   # video url, phone number login
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha()
        }

        # time.sleep(3)

    else:
        # 判断用户名是否为邮箱
        if "@" in account:   # if re.match("^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$", account):   # match e-mail
            print("邮箱方式登陆")
            post_url = "https://www.zhihu.com/login/email"    # email login
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
                "captcha": get_captcha()
            }
    # create post request
    response_text = session.post(post_url, data=post_data, headers=header)
    # print(response_text.text)    # 返回验证码会话无效,需要处理验证码问题, learn 5-16 5-17
    session.cookies.save()


if __name__ == '__main__':
    # get_xsrf()
    # zhihu_login("te", "")
    username = input("Pleaes input username:\n")
    password = input("Pleaes input password:\n")
    # print(type(username))   # <class 'str'>
    zhihu_login(username, password)
    # get_captcha()
    print(is_login())   # return test result
    # get_index()


