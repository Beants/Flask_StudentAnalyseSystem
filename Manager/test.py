#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/8 7:21 PM
# @Author : maxu
# @Site : 
# @File : test.py
# @Software: PyCharm

from pyecharts import Bar

bar = Bar("我的第一个图表", "这里是副标题")
bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
# bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
html = bar # 生成本地 HTML 文件
print(bar)