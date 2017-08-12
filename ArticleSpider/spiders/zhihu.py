# -*- coding: utf-8 -*-

import re
import json

# from urllib import parse      # python3, python2 use "import urlparse"
# 兼容的import写法

try:
    import urlparse as parse
except:
    from urllib import parse


import scrapy

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
        """
        提取出html页面中的所有url 并跟踪这些url进行进一步爬取
        如果提取的url中格式为/question/xxx 就下载之后直接进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]    # 通过response.url获取主域名
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            # print(url)     # for Debug
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                # print(request_url, question_id)    # for Debug

                # scrapy中通过yield将requests提交给下载器
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)

    def parse_question(self, response):
        # 处理question页面，从页面中提取出具体的question item
        # 01:45
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

        # Attention Security
        zhihu_username = "Your zhihu username"
        zhihu_password = "Your zhihu password"
        zhihu_username = "1"
        zhihu_password = "-"


        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"  # video url, phone number login
            post_data = {
                "_xsrf": xsrf,
                "phone_num": zhihu_username,
                "password": zhihu_password,
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


