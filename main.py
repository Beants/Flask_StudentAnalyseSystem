#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/6 4:23 PM
# @Author : maxu
# @Site : 
# @File : main.py.py
# @Software: PyCharm

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    return render_template('search.html')


@app.route('/dataManager/')
def dataManager():
    return render_template('dataManager.html')


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
    app.run(debug=True)
