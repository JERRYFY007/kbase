# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:task.py
# @time:2017/6/8
#
#  知识库局部同义词的处理
from .segment import *


class User:
    def __init__(self):
        self.id = []

    def f(self):
        return 'hello world'


@app.route('/task', methods=['GET', 'POST'])
@app.route('/task/', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        question = request.form.get('question')
        app.logger.info("Question: %s", question)
        dict_slot = {}

        app.logger.info("Question Segmation: %s")
        return render_template('task.html', task=True, question=question, slot=dict_slot, )
    return render_template('task.html',)
