#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'TesterCC'
# __time__   = '17/10/6 21:13'


from zheye import zheye
z = zheye()
positions = z.Recognize('captcha_cn.gif')

print(positions)
# (y1,x1),(y2,x2)       坐标第二个值是x轴
# positions = [(49.131726816653426, 83.154534350613588), (46.515652833013959, 167.37939761132762)]
# positions[0][0] = 49.131726816653426
# positions[0][1] = 83.154534350613588
# positions[1][0] = 46.515652833013959
# positions[1][1] = 167.37939761132762



