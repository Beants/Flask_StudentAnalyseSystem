#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/6 4:23 PM
# @Author : maxu
# @Site : 
# @File : main.py.py
# @Software: PyCharm

from flask import Flask, render_template, request
from pyecharts import Overlap

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
        from pyecharts import Bar, Line
        from pyecharts_javascripthon.api import TRANSLATOR

        REMOTE_HOST = "https://pyecharts.github.io/assets/js"

        data, len_data = mongo.get_data_by_condition(request.args.get('stuID'))
        data_day_out = {}
        data_day_in = {}
        import time
        fun = lambda year, month: list(
            range(1, 1 + time.localtime(time.mktime((year, month + 1, 1, 0, 0, 0, 0, 0, 0)) - 86400).tm_mday))
        days = fun(2017, 11)
        # for i in days:
        #     if i < 10:
        #         index = days.index(i)
        #         days[index] = int('0' + str(i))
        # print(days)
        for item in days:
            # '2017-11-' +
            data_day_in[str(item)] = 0
            data_day_out[str(item)] = 0

        for item in data:
            time = str(int(str(item[4]).split(' ')[0].split('-')[2]))
            # print(time)
            money = -float(item[3])
            if money > 0:
                data_day_out[time] += money
                data_day_out[time] = float(format(data_day_out[time], '.2f'))
            else:
                data_day_in[time] += money
                data_day_in[time] = float(format(data_day_in[time], '.2f'))
        bar = Bar("", "")

        bar.add('消费金额', days, list(data_day_out.values()))
        bar.add('充值金额', days, list(data_day_in.values()), bar_category_gap=0.05)
        line = Line()

        line.add("消费均值", days, [format(sum(list(data_day_out.values())) / len(days), '.2f')] * list(
            data_day_out.values()).__len__())
        # line.add("消费均值", days,
        #          sum(list(data_day_out.values())) / (list(data_day_out.values()).__len__()))  # print(len_data)

        overlap = Overlap()
        overlap.add(bar)
        overlap.add(line)
        javascript_snippet = TRANSLATOR.translate(overlap.options)

        no_out_days_num = 0
        no_out_days = []
        for i in data_day_out.keys():
            if data_day_out[i] == 0:
                no_out_days_num += 1
                no_out_days.append(str(list(data_day_out.keys()).index(i)) + '号')
            else:
                print(i)
                '''
                max             最大值
                min             最小值
                avg             平均值
                in              充值金额
                not_eat_days    没有消费的天数
                
                
                '''
        res_analyse = {
            'max': format(max(list(data_day_out.values())), '.2f'),
            'min': format(min(list(data_day_out.values())), '.2f'),
            'avg': format(sum(list(data_day_out.values())) / len(days), '.2f'),
            'sum_in': format(-sum(list(data_day_in.values())), '.2f'),
            'sum_out': format(sum(list(data_day_out.values())), '.2f'),
            'no_out_days_num': no_out_days_num,
            'no_out_days': no_out_days.__str__().replace('[', '').replace(']', '').replace("'", ''),
        }
        return render_template('dataManagerStudent.html',
                               data=res_analyse,
                               chart_id=overlap.chart_id,
                               host=REMOTE_HOST,
                               renderer=overlap.renderer,
                               my_width="100%",
                               my_height=600,
                               custom_function=javascript_snippet.function_snippet,
                               options=javascript_snippet.option_snippet,
                               script_list=overlap.get_js_dependencies())


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
