# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:dialog.py
# @time:2017/4/10 0010 16:04
from flask import render_template, request
from app import *
from .segment import *
from lxml import etree


def fmmcut(sentence, wordsdict1, wordsdict2, wordsdict3, FMM=True):
    result_s = []
    sentence = sentence.lower()
    s_length = len(sentence)
    if FMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict1:
                    synonym = wordsdict1.get(word)
                    result_s.append("@" + synonym + "," + str(wordsdict2.get(synonym)))
                    sentence = sentence[w_length:]
                    break
                elif word in wordsdict2:
                    result_s.append("@" + word + "," + str(wordsdict2.get(word)))
                    sentence = sentence[w_length:]
                    break
                elif word in wordsdict3 or w_length == 1:
                    result_s.append(word)
                    sentence = sentence[w_length:]
                    break
                else:
                    word = word[:w_length - 1]
                w_length = w_length - 1
            s_length = len(sentence)
    else:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict1:
                    synonym = wordsdict1.get(word)
                    result_s.insert(0, ("@" + synonym + "," + str(wordsdict2.get(synonym))))
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in wordsdict2:
                    result_s.insert(0, ("@" + word + "," + str(wordsdict2.get(word))))
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in wordsdict2 or w_length == 1:
                    result_s.insert(0, word)
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
    return result_s


def load_keyword_dict(xml_filename):
    print("Building Keyword & Synonym dictionary...")
    root = etree.parse(xml_filename).getroot()
    keyword_no, synonym_no = 0, 0
    importance = 0.0
    dict_keyword, dict_synonym = {}, {}
    for keyword in root:
        row_data = []
        for item in keyword:
            row_data.append(item.text.strip())
        while len(row_data) >= 3:
            synonym_no += 1
            value = row_data[0].lower()
            synonym = row_data[-1].lower()
            importance = float(row_data[1])
            dict_keyword[value] = importance
            dict_synonym[synonym] = value
            row_data.pop(-1)
        if len(row_data) == 2:
            keyword_no += 1
            value = row_data[0].lower()
            importance = float(row_data[1])
            dict_keyword[value] = importance
    print('Process Keyword: ', keyword_no)
    print('Process Synonym: ', synonym_no)
    print('Process Keyword Dict: ', len(dict_keyword))
    print('Process Synonym Dict: ', len(dict_synonym))
    print("The volumn of Keyword & Synonym dictionary:", len(dict_keyword), len(dict_synonym))
    return dict_keyword, dict_synonym


def load_extend_dict(xml_filename):
    print("Building Extend & Knownledge dictionary...")
    root = etree.parse(xml_filename).getroot()
    qa_id, ex_no = 0, 0
    dict_question, dict_answer = {}, {}
    dict_extend, dict_extend_item, dict_extend_point = {}, {}, {}
    for knowledge in root:
        qa_id = qa_id + 1
        qa_data = []
        ex_id = 0
        for field in knowledge:
            if field.text is None:
                ex_id = ex_id + 1
                extend_item = []
                qa_ex = str(qa_id) + ':' + str(ex_id)
                for item in field:
                    dict_extend_point[qa_ex] = 0.0
                    row_data = []
                    for keyword in item:
                        row_data.append(keyword.text.strip())
                        extend_item.append(keyword.text.strip())
                    while len(row_data) >= 3:
                        extend = row_data[-1].lower()
                        extend_item.append(extend)
                        if extend in dict_extend:
                            temp = dict_extend.get(extend)
                            temp.append(qa_ex)
                            dict_extend[extend] = temp
                        else:
                            temp = []
                            temp.append(qa_ex)
                            dict_extend[extend] = temp
                        row_data.pop(-1)
                    if len(row_data) == 2:
                        extend = row_data[0].lower()
                        if extend in dict_extend:
                            temp = dict_extend.get(extend)
                            temp.append(qa_ex)
                            dict_extend[extend] = temp
                        else:
                            temp = []
                            temp.append(qa_ex)
                            dict_extend[extend] = temp
                if extend_item:
                    dict_extend_item[qa_ex] = extend_item
            else:
                qa_data.append(field.text.strip())
        ex_no += ex_id
        dict_question[qa_id] = qa_data[0]
        dict_answer[qa_id] = qa_data[1]
    print("Process Extend Dict: ", len(dict_extend))
    print("Process QA: ", qa_id)
    print("Process Extend: ", ex_no)
    print("The volumn of Extend & Knownledge dictionary:", len(dict_extend), len(dict_extend_point), len(dict_extend_item), len(dict_answer))
    return dict_extend, dict_extend_point, dict_extend_item, dict_answer


def countPoint(items):
    best, max, match, unmatch = 0.0, 0.0, 0.0, 0.0   # 最佳分，最高分，匹配分，不匹配分
    point = 0.0   # 当前分
    for i in dict_extend_item:
        for item in dict_extend_item.get(i):
            if item in items:
                match += dict_keyword.get(item)
                dict_extend_point[i] += dict_keyword.get(item)
            elif item in dict_keyword:
                unmatch -= dict_keyword.get(item)
                dict_extend_point[i] -= dict_keyword.get(item)
        if dict_extend_point[i] > 0:
            print(dict_extend_point[i], dict_extend_item[i])

    for item in items:
        if item in dict_extend:
            for qa_ex in dict_extend.get(item):
                p = dict_keyword.get(item)
                dict_extend_point[qa_ex] = dict_extend_point.get(qa_ex) + dict_keyword.get(item)
    for i in dict_extend_point:
        if dict_extend_point.get(i) > max:
            max = dict_extend_point.get(i)
            # print(i, dict_extend_point.get(i))
    return

dict_extend, dict_extend_point, dict_extend_item, dict_answer = load_extend_dict("app/dict/knowledge.xml")
dict_keyword, dict_synonym = load_keyword_dict("app/dict/keyword.xml")


@app.route('/dialog', methods=['GET', 'POST'])
@app.route('/dialog/', methods=['GET', 'POST'])
def dialog():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = []
        items = []
        point = 0.0

        fmm1 = fmmcut(question, wordsdict1, wordsdict2, wordsdict3)
        print(fmm1)
        answer.append(fmm1)
        for word in fmm1:
            if '@' in word:
                word, importance = word.strip().split(',')
                _, word = word.strip().split('@')
                print(word, importance)
                answer.append(word + ' ' + importance)
                items.append(word)
        point = countPoint(items)
        # print(point)
        return render_template('dialog.html', dialog = True, question = question, answers = answer, )
    return render_template('dialog.html',)
