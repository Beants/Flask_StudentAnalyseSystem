#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/6 4:23 PM
# @Author : maxu
# @Site : 
# @File : main.py.py
# @Software: PyCharm

from flask import Flask, render_template, request
from pyecharts import Grid, Overlap, Line

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

        REMOTE_HOST = "https://pyecha rts.github.io/assets/js"

        data, len_data = mongo.get_data_by_condition(request.args.get('stuID'))
        data_day_out = {}
        data_day_in = {}
        data_shop = []
        data_shop_money = {}  # 这个月花费的金额
        data_shop_num = {}  # 这个月消费的次数
        data_shop_money_avg = {}  # 每次消费平均金额
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
            shop = str(item[2])
            if shop == '407010002':
                pass
            else:
                shop = shop.replace(str(item[2])[:3], str(item[2])[:3] + '\n')
                if shop not in data_shop:
                    data_shop.append(shop)
                    data_shop_money[shop] = money
                    data_shop_money[shop] = float(format(data_shop_money[shop], '.2f'))
                    data_shop_num[shop] = 1
                else:
                    data_shop_money[shop] += money
                    data_shop_money[shop] = float(format(data_shop_money[shop], '.2f'))
                    data_shop_num[shop] += 1
            if money > 0:
                data_day_out[time] += money
                data_day_out[time] = float(format(data_day_out[time], '.2f'))
            else:
                data_day_in[time] += money
                data_day_in[time] = float(format(data_day_in[time], '.2f'))

        # data_shop = data_shop.sort()
        # 计算每次在店消费的平均值
        for i in data_shop:
            data_shop_money_avg[i] = float(format(data_shop_money[i] / data_shop_num[i], '.2f'))
        # data_shop.pop(data_shop.index('407010002'))
        # data_shop_money.pop('407010002')
        # data_shop_num.pop('407010002')
        # data_shop_money_avg.pop('407010002')
        # 拼接返回值
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

        ##########图

        bar = Bar(height=600)  # 柱形图

        bar.add('消费金额', days, list(data_day_out.values()), mark_line=["average"], mark_point=["max", "min"],
                )
        bar.add('充值金额', days, list(data_day_in.values()), bar_category_gap=0.05, mark_line=["average"],
                mark_point=["max", "min"])

        overlap = Overlap()
        bar2 = Bar("消费地点分析", title_top="50%", )
        bar2.add('消费金额', data_shop, list(data_shop_money.values()), mark_point=["max", "min"], legend_top="50%")
        bar2.add('消费次数', data_shop, list(data_shop_num.values()), mark_point=["max", "min"], legend_top="50%")

        line = Line()
        line.add('消费均值', data_shop, list(data_shop_money_avg.values()), legend_top="50%", mark_point=["max", "min"])

        overlap.add(bar2)
        overlap.add(line)
        grid = Grid()
        grid.add(bar, grid_bottom="60%")
        grid.add(overlap, grid_top="60%")

        javascript_snippet = TRANSLATOR.translate(grid.options)


        return render_template('dataManagerStudent.html',
                               data=res_analyse,
                               chart_id=grid.chart_id,
                               host=REMOTE_HOST,
                               renderer=grid.renderer,
                               my_width="100%",
                               my_height=1200,
                               custom_function=javascript_snippet.function_snippet,
                               options=javascript_snippet.option_snippet,
                               script_list=grid.get_js_dependencies())


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
