# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:task.py
# @time:2017/6/8
#
#  知识库局部同义词的处理
from flask import render_template, request
from app import *
from .segment import *


@app.route('/task', methods=['GET', 'POST'])
@app.route('/task/', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        question = request.form.get('question')
        app.logger.info("Question: %s", question)
        dict_seg = {}
        app.logger.info("Question Segmation: %s")
        return render_template('task.html', qa = True, question = question, seg = dict_seg,  )
    return render_template('task.html',)
