# -*- coding: utf-8 -*-

import re
import json
import datetime

# from urllib import parse      # python3, python2 use "import urlparse"
# 兼容Python2和Python3的import写法

try:
    import urlparse as parse    # Python2
except:
    from urllib import parse    # Python3

import scrapy
from scrapy.loader import ItemLoader
from zheye import zheye

from items import ZhihuQuestionItem, ZhihuAnswerItem


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

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        """
        提取出html页面中的所有url 并跟踪这些url进行进一步爬取
        如果提取的url中格式为/question/xxx 就下载之后直接进入解析函数
        其实是深度优先的爬虫逻辑
        1.提取出全部的URL
        2.过滤出不需要的URL
        3.然后在剩下的URL中遍历，发现question url就进一步跟踪
        4.item到pipeline，request路由到下载器进行下载
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
                # break  # for debug answer
            else:
                # 如果不是question页面则直接进一步跟踪
                # pass    # comment for debug answer
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

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers, callback=self.parse_answer)
        yield question_item   # comment for debug answer

    def parse_answer(self, response):
        # 处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]    # 判断后续是否还有页面需要请求
        # total_answer = ans_json["paging"]["totals"]
        next_url = ans_json["paging"]["is_end"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item['zhihu_id'] = answer["id"]
            answer_item['url'] = answer["url"]
            answer_item['question_id'] = answer["question"]["id"]
            answer_item['author_id'] = answer["author"]["id"] if "id" in answer["author"] else None   # 匿名提问者现在是id=0
            answer_item['content'] = answer["content"] if "content" in answer else None
            answer_item['praise_num'] = answer["voteup_count"]
            answer_item['comments_num'] = answer["comment_count"]
            answer_item['create_time'] = answer["created_time"]
            answer_item['update_time'] = answer["updated_time"]
            answer_item['crawl_time'] = datetime.datetime.now()    # current time

            yield answer_item     # yield出去交给pipeline处理

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    # crawler entery
    def start_requests(self):
        # get_xsrf method1，用之前写的zhihu_login_requests.py - def get_xsrf()
        # get xsrf method2, 利用scrapy提供的异步URL
        # https://www.zhihu.com/#signin  login page
        return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.headers, callback=self.login)]     # 异步io用callback执行下一步

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
        username = input("Please input username(phone):\n>>")     # only mobile phone，因为下面post_url访问的是phone_num登录入口
        password = input("Please input password:\n>>")

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

            # debug recognize Chinese captcha
            captcha_url_cn = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=cn".format(t)
            yield scrapy.Request(captcha_url_cn, headers=self.headers, meta={"post_data": post_data},
                                 callback=self.login_after_captcha_cn)

            # 下面可打breakpoint debug -- comment because use captcha_url_cn can auto login, use Machine Learning.
            # yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data},
            #                      callback=self.login_after_captcha)  # self.login_after_cpatcha()

    # 特别处理
    def login_after_captcha_cn(self, response):
        # 知乎倒立汉字验证识别码登录
        # 1st -- save captcha pic
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)  # different from scrapy
            f.close()

        # 2ed -- use zheye to recognize coordinate
        z = zheye()
        positions = z.Recognize('captcha.jpg')
        print(positions)   # for debug

        # 3rd -- judge coordinate   处理顺序比较好，因为有的验证码要求按顺序点击
        pos_arr = []
        if len(positions) == 2:
            if positions[0][1] > positions[1][1]:        # [(y2,x2),(y1,x1)]
                pos_arr.append([positions[1][1], positions[1][0]])      # 第一个坐标 (x1,y1)
                pos_arr.append([positions[0][1], positions[0][0]])      # 第二个坐标 (x2,y2)
            else:
                pos_arr.append([positions[0][1], positions[0][0]])
                pos_arr.append([positions[1][1], positions[1][0]])
        else:
            # 如果仅有一个文字倒立
            pos_arr.append([positions[0][1], positions[0][0]])     # (x, y)

        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = response.meta.get("post_data", {})

        # pos_arr坐标顺序已经调整为正常(x,y),故可正常提取
        # 判断是一个坐标还是两个坐标
        if len(positions) == 2:
            post_data["captcha"] = '{"img_size": [200, 44], "input_points": [[%.2f, %f],[%.2f, %f]]}' % (pos_arr[0][0] / 2, pos_arr[0][1] / 2, pos_arr[1][0]/2, pos_arr[1][1] / 2)
        else:
            post_data["captcha"] = '{"img_size": [200, 44], "input_points": [[%.2f, %f]}' % (pos_arr[0][0] / 2, pos_arr[0][1] / 2)

        # 保证正确率，设置captcha_type
        post_data["captcha_type"] = "cn"

        # FormRequest()可以完成表单提交
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login  # 不传递函数调用，只传递函数名称
        )]

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
            # im.close()   # 可以注释，会报错  或者except: pass
        except:
            return "Image Handle Error."

        captcha = input("请输入英文字母验证码\n>>")

        # post data logic
        post_data = response.meta.get("post_data", {})
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
        if "msg" in text_json and text_json["msg"] == "登录成功":           # 登录失败则爬虫停止
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)    # headers很重要，不写callback=XX,回调默认调parse()


