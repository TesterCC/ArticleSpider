#!/usr/bin/env python
# coding=utf-8
__author__ = 'Lily'

import hashlib


def get_md5(url):
    if isinstance(url, str):     # python3 str default use unicode
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()   # 抽取其摘要

if __name__ == '__main__':
    print(get_md5("http://blog.jobbole.com/".encode("utf-8")))  # urlstr.encode("utf-8")
    print(get_md5("http://blog.jobbole.com/"))  # urlstr.encode("utf-8")