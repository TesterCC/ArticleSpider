# -*- coding: utf-8 -*-

import re
import json

# from urllib import parse      # python3, python2 use "import urlparse"
# 兼容Python2和Python3的import写法

try:
    import urlparse as parse    # Python2
except:
    from urllib import parse    # Python3

import scrapy

from scrapy.loader import ItemLoader
from ..items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    # question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

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
                # 如果提取到question相关的页面则下载后交由提取函数parse_question进行提取
                request_url = match_obj.group(1)
                # question_id = match_obj.group(2)
                # print(request_url, question_id)    # for Debug

                # scrapy中通过yield将requests提交给下载器
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)   # 不写callback=XX也可以,回调默认会调parse()

    def parse_question(self, response):
        # 处理question页面，从页面中提取出具体的question item

        if "QuestionHeader-title" in response.text:
            # 处理新版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))  # question_id在数据库中是int类型，传入前最好先处理好

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")    # 取html内容，不用伪类选择器
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-value::text")    # return a list
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")   # 子带元素中寻找元素  div是后代节点，多少层都能找
            # item_loader.add_xpath("topics", "//*[@id='root']/div/main/div/meta[3]")    # 提取的整个标签, 可以考虑以后用正则表达式处理
            question_item = item_loader.load_item()
            pass
        else:
            # 处理知乎旧版本页面的item提取 -- 实际现在应该都是新版本了。
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))  # question_id在数据库中是int类型，传入前最好先处理好
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", ".zh-question-title h2 a::text")
            item_loader.add_css("content", "#zh-question-detail")  # #zh中#表示取的id
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")  # return a list
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")  # 子带元素中寻找元素

            question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        # 处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]    # 判断后续是否还有页面需要请求  ＃2:31

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
        # username = input("Pleaes input username:\n>>")     # e-mail or mobile phone number
        # password = input("Pleaes input password:\n>>")
        username = ("13551856640")     # only email，因为下面post_url访问的是phone_num登录入口
        password = ("-TesterCC07-")

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"  # video url, phone number login
            post_data = {
                "_xsrf": xsrf,
                "phone_num": username,
                "password": password,
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
            # im.close()   # 可以注释，会报错
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


