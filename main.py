#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/6 4:23 PM
# @Author : maxu
# @Site : 
# @File : main.py.py
# @Software: PyCharm

from flask import Flask, render_template, request

import config
import mongo

app = Flask(__name__)

app.config.from_object(config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    return render_template('search.html')


@app.route('/dataManager/student', methods=["POST", "GET"])
def dataManagerStudent():
    stuID = (request.args.get('stuID'))
    if stuID == None:
        return render_template('dataManagerStudent.html', data=None)
    else:
        from pyecharts import Bar
        from pyecharts_javascripthon.api import TRANSLATOR
        REMOTE_HOST = "https://pyecharts.github.io/assets/js"

        bar = Bar("我的第一个图表", "这里是副标题")
        bar.add(
            "服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90]
        )

        javascript_snippet = TRANSLATOR.translate(bar.options)


        data, len_data = mongo.get_data_by_condition(request.args.get('stuID'))
        data_day = {}
        for item in data:
            time = str(item[4]).split(' ')
            money = -float(item[3])
            if time not in data_day.keys():
                data_day[time] = money

        print(len_data)
        return render_template('dataManagerStudent.html', data=data, chart_id=bar.chart_id,
                               host=REMOTE_HOST,
                               renderer=bar.renderer,
                               my_width="100%",
                               my_height=600,
                               custom_function=javascript_snippet.function_snippet,
                               options=javascript_snippet.option_snippet,
                               script_list=bar.get_js_dependencies(), )


@app.route('/dataManager/')
def dataManager():
    return render_template('dataManager.html')


@app.route('/dataManager/class')
def dataManagerClass():
    return render_template('dataManagerClass.html')

@app.route('/search_result', methods=['GET'])
def search_result():
    request.encoding = 'utf-8'
    context = {}
    try:

        import mongo
        print(request.args.get('stuID'), request.args.get('className'), request.args.get('shop'),
              request.args.get('postingDate'))

        data, len_data = mongo.get_data_by_condition(request.args.get('stuID'), request.args.get('className'),
                                               request.args.get('shop'),
                                               request.args.get('postingDate'))

        # if len_data=
        context['data'] = data
        context['len_data'] = len_data
        print('context ', context)

    except IndexError:
        print('没有')
        context['data'] = False
        print(context)
    return render_template('search_result.html', content=context)


if __name__ == '__main__':
    app.run()
