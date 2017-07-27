# -*- coding: utf-8 -*-

import re
import scrapy
import json


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": agent
    }

    def parse(self, response):
        pass

    def parse_detail(self, response):
        # 解析真正需要解析数据的页面
        pass

    def start_requests(self):
        # get_xsrf method1，用之前写的zhihu_login_requests.py - def get_xsrf()
        # get xsrf method2, 利用scrapy提供的异步URL
        # https://www.zhihu.com/#signin  login page
        return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.headers, callback=self.login)]

    def login(self, response):
        response_text = response.text

        # match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)  # need to add flags
        match_obj = re.match('(.*)', response.text, re.DOTALL)  # display all content  #without re.DOTALL, just match a line.
        xsrf = ""
        if match_obj:
            # print(match_obj.group(1))
            xsrf = match_obj.group(1)
        else:
            return "Match failed."

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"  # video url, phone number login
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "13551856640",
                "password": "-TesterCC07-",
                "captcha": ""
            }

            import time

            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=en".format(t)
            # 下面可打breakpoint debug
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data}, callback=self.login_after_captcha)  # self.login_after_cpatcha()

# 也可以从response中拿到cookie，再设置到request中，是另外一种解决方案，这里未实现
    def login_after_captcha(self, response):
        # save captcha pic logic
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)      # different from scrapy
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            return "Image Handle Error."

        captcha = input("请输入英文字母验证码\n>>")

        post_data = response.meta.get("post_data")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha


        # FormRequest()可以完成表单提交
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login  # 不传递函数调用，只传递函数名称
        )]

    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)     # 反序列化 byte -> obj
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)    # 不写callback=XX,回调默认调parse()


