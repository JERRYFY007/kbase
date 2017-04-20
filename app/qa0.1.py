# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:dialog.py
# @time:2017/4/10 0010 16:04
from flask import render_template, request
from app import *
from .segment import *
from lxml import etree
import pandas as pd
from pandas.io.parsers import read_csv


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


def load_dataframe(xml_filename):
    print("Building  Extend & Keyword Dataframe...")

    # Process knowledge.xml
    tree = etree.parse(xml_filename)
    root = tree.getroot()
    extends = {}
    qa_ex, items, local_synonym = [], [], []
    keyword_value, importance, global_synonym = [], [], []
    qa_id, ex_no, kw_no, sy_no = 0, 0, 0, 0
    for knowledge in root:
        qa_id = qa_id + 1
        ex_id = 0
        for field in knowledge:
            if field.text is None:
                ex_id = ex_id + 1
                kw_id = 0
                qa_ex_id = str(qa_id) + ':' + str(ex_id)
                for item in field:
                    row_data = []
                    kw_id += 1
                    for keyword in item:
                        row_data.append(keyword.text.strip())
                    sy_no += len(row_data) - 2
                    if len(row_data) == 2:
                        qa_ex.append(qa_ex_id)
                        items.append(row_data[0].lower())
                        local_synonym.append('')
                    elif len(row_data) >= 3:
                        qa_ex.append(qa_ex_id)
                        items.append(row_data[0].lower())
                        local_synonym.append(row_data[-1])
                kw_no += kw_id
    extends['qa_id:ex_id'] = qa_ex
    extends['Item'] = items
    extends['synonym'] = local_synonym
    df_extend = pd.DataFrame(extends)
    df_keyword = read_csv("app/dict/keyword.dict", encoding='utf8')
    df_extend = pd.merge(df_extend, df_keyword, how='left', on='Item')
    print("The volumn of Extend & Keyword Dataframe:", len(df_extend), len(df_keyword))
    return df_extend, df_keyword


def load_qa(xml_filename):
    print("Building Question & Answer Dict...")
    # Process knowledge.xml
    tree = etree.parse(xml_filename)
    root = tree.getroot()
    dict_question, dict_answer = {}, {}
    qa_id = 0
    for knowledge in root:
        qa_id = qa_id + 1
        qa_data = []
        for field in knowledge:
            if field.text is None:
                continue
            else:
                qa_data.append(field.text.strip())
        dict_question[qa_id] = qa_data[0]
        dict_answer[qa_id] = qa_data[1]
    print("The volumn of Question & Answer Dict:", len(dict_question), len(dict_answer))
    return dict_question, dict_answer


def countPoint(df_extend, df_seg):
    best, match, unmatch = 0.0, 0.0, 0.0   # 最佳分，最高分，匹配分，不匹配分
    point = 0.0   # 当前分
    print("df_seg in def", df_seg)
    # df_extend = pd.merge(df_extend, df_keyword, how='left', on='Item')
    df = pd.merge(df_extend, df_seg, how='left', on='Item')
    df_qa_ex = pd.merge(df_extend, df_seg, how='right', on='Item')

    dict_qa_point = {}
    for qa in df_qa_ex['qa_id:ex_id']:
        df_qa = df.loc[df['qa_id:ex_id'] == qa,]
        dict_qa_point[qa] = df_qa['im'].sum() * 2 - df_qa['importance'].sum()

    print(len(dict_qa_point))
    for k, v in dict_qa_point.items():
        if v > 1:
            print(k, v)

    match_id = []
    match = max(dict_qa_point, key=dict_qa_point.get)
    match_id.append(match)
    print("MAX1: ", match, dict_qa_point[match])
    dict_qa_point.pop(match)
    match = max(dict_qa_point, key=dict_qa_point.get)
    match_id.append(match)
    print("MAX2: ", match, dict_qa_point[match])
    dict_qa_point.pop(match)
    match = max(dict_qa_point, key=dict_qa_point.get)
    match_id.append(match)
    print("MAX3: ", match, dict_qa_point[match])
    dict_qa_point.pop(match)
    match = max(dict_qa_point, key=dict_qa_point.get)
    match_id.append(match)
    print("MAX4: ", match, dict_qa_point[match])
    print(match_id)
    return match_id


def get_qa(dict_question, dict_answers, items):
    questions, answers = [], []
    i = 0
    for item in items:
        qa_id, ex_id = item.strip().split(':')
        print(qa_id, ex_id)
        if int(qa_id) in dict_question:
            print("Find question & answer!", i)
            i += 1
            questions.append(str(i) + ':' + dict_question.get(int(qa_id)))
            answers.append(str(i) + ':' + dict_answers.get(int(qa_id)))
    return questions, answers

df_extend, df_keyword = load_dataframe("app/dict/knowledge.xml")
dict_question, dict_answer = load_qa("app/dict/knowledge.xml")


def CountPoint():
    max =0

    return

@app.route('/qa', methods=['GET', 'POST'])
@app.route('/qa/', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = {}
        best_question, best_answer = [], []
        items = []

        fmm1 = fmmcut(question, wordsdict1, wordsdict2, wordsdict3)
        print(fmm1)
        # answer.append('Item,im')
        item, im = [], []
        for word in fmm1:
            if '@' in word:
                word, importance = word.strip().split(',')
                _, word = word.strip().split('@')
                # print(word, importance)
                item.append(word)
                im.append(float(importance))
        answer['Item'] = item
        answer['im'] = im
        # print(answer, item, im)
        df_seg = pd.DataFrame(answer)
        print(df_seg)
        items = countPoint(df_extend, df_seg)
        print(items)
        best_question, best_answer = get_qa(dict_question, dict_answer, items)
        print(best_question, best_answer)
        return render_template('qa.html', qa = True, questions = best_question, answers = best_answer, )
    return render_template('qa.html',)
