#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/6 21:13'


from zheye import zheye
z = zheye()
positions = z.Recognize('captcha_cn.gif')

print(positions)

