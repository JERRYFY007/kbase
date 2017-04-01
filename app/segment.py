# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:view.py
# @time:2017/3/29
from flask import render_template, request
from app import app

import jieba
import jieba.analyse

@app.route('/segment', methods=['GET', 'POST'])
@app.route('/segment/', methods=['GET', 'POST'])
def segment():
    if request.method == 'POST':
        segment = request.form.get('sentence')
        #print(segment)
        cut0 = jieba.cut_for_search(segment)  # 搜索引擎模式
        cut1 = jieba.cut(segment, cut_all=True)  # 全模式
        cut2 = jieba.cut(segment, cut_all=False)  # 默认模式
        cut3 = jieba.cut(segment)  #
        segmented = []
        segmented.append('/'.join(cut0))
        segmented.append('/'.join(cut1))
        segmented.append('/'.join(cut2))
        segmented.append('/'.join(cut3))
        analyse = []
        for x, w in jieba.analyse.extract_tags(segment, withWeight=True):
            analyse.append('%s %s' % (x, w))
        for x, w in jieba.analyse.textrank(segment, withWeight=True):
            analyse.append('%s %s' % (x, w))
        return render_template('segment.html', sentence=segment, segmented=segmented, analyse=analyse)
    return render_template('segment.html')