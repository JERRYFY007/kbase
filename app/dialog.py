# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:dialog.py
# @time:2017/4/10 0010 16:04
from flask import render_template, request
from app import *
from .segment import *


@app.route('/dialog', methods=['GET', 'POST'])
@app.route('/dialog/', methods=['GET', 'POST'])
def dialog():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = []
        answer.append(''.join(mmcut(question, wordsdict1, wordsdict2, wordsdict3, RMM=False)))
        return render_template('dialog.html', dialog = True, question = question, answer = answer, )
    return render_template('dialog.html',)
