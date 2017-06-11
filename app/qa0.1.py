# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:qa.py
# @time:2017/6/8
#
#  知识库局部同义词的处理
from flask import render_template, request
from app import *
from .segment import *
from lxml import etree


def gen_dict_synonym(dictfile):
    print("Building dictionary...")
    dictionary = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, item = line.strip().lower().split(',')
            if item != 'Item':
                dictionary[word] = item
    f.close()
    print("The volumn of global synonym dictionary: %d" % (len(dictionary)))
    return dictionary


def gen_dict_local_synonym(dictfile):
    print("Building dictionary...")
    dictionary = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, item = line.strip().lower().split(',')
            if item != 'Item':
                dictionary[word] = item
    f.close()
    print("The volumn of loacal synonym dictionary: %d" % (len(dictionary)))
    return dictionary


def fmmcut(sentence, dict_kw, dict_global_sy, dict_local_sy, FMM = True):
    result_s = []
    sentence = sentence.lower()
    s_length = len(sentence)
    if FMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in dict_kw:
                    result_s.append("@" + word + "," + str(dict_kw.get(word)))
                    sentence = sentence[w_length:]
                    break
                # 处理global synonym word
                elif word in dict_global_sy:
                    print("Find a global synonym word: ", word)
                    result_s.append("@" + dict_global_sy.get(word) +  ',' + str(dict_kw.get(word)))
                    sentence = sentence[w_length:]
                    break
                # 处理local synonym word
                elif word in dict_local_sy:
                    print("Find a local synonym word: ", word)
                    result_s.append("#" +  word + "," + dict_local_sy.get(word))
                    sentence = sentence[w_length:]
                    break
                elif w_length == 1:
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
                if word in dict_kw:
                    result_s.insert(0, ("@" + word + "," + str(dict_kw.get(word))))
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in dict_global_sy or w_length == 1:
                    result_s.insert(0, word)
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
    return result_s


def load_dataframe():
    dict_keyword = {}
    with open("app/dict/keyword.dict", encoding='utf8') as f:
        for line in f:
            (val, imp) = line.strip().split(',')
            dict_keyword[val] = imp
    dict_extend_item = {}
    with open("app/dict/extend_item.dict", encoding='utf8') as f:
        for line in f:
            (qa_ex_id, item) = line.strip().split(',')
            dict_extend_item[qa_ex_id] = item
    return dict_keyword, dict_extend_item


def load_qa(xml_filename):
    print("Building Question, Answer, Branch Dict...")
    # Process knowledge.xml
    tree = etree.parse(xml_filename)
    root = tree.getroot()
    dict_question, dict_answer, dict_branch = {}, {}, {}
    qa_id = 0
    for knowledge in root:
        qa_id = qa_id + 1
        br_id = 0
        for field in knowledge:
            if field.tag == "question":
                dict_question[qa_id] = field.text
            if field.tag == "answer":
                dict_answer[qa_id] = field.text
            if field.tag == "branch":
                br_id += 1
                dict_branch[str(qa_id) + ':' + str(br_id)] = field.text
    print("The volumn of Question & Answer Dict:", len(dict_question), len(dict_answer))
    return dict_question, dict_answer, dict_branch

dict_keyword, dict_extend_item = load_dataframe()
dict_question, dict_answer, dict_branch= load_qa("app/dict/knowledge.xml")


def get_qa(items):
    question, answer, branch = [], [], []
    if len(items) > 4:
        max5 = 4
    else:
        max5 = len(items)
    for j in range(max5):
        qa_id = items[j]
        if int(qa_id) in dict_question:
            # print("Find question & answer!")
            question.append(dict_question.get(int(qa_id)))
            answer.append(dict_answer.get(int(qa_id)))
            branch.append(dict_branch.get(qa_id))
    return question, answer, branch


def CountPoint(dict_seg):
    with open("app/dict/extend_point.df", encoding='utf8') as f:
        best_id, best = [''], [0.0]
        for line in f:
            (qa_ex_id, _, _, _, _) = line.strip().split(',')
            point, max, match, unmatch = 0.0, 0.0, 0.0, 0.0
            if dict_extend_item.get(qa_ex_id) and (dict_extend_item.get(qa_ex_id) != 'Item'):
                items = dict_extend_item.get(qa_ex_id).split(';')
                items.pop(-1)
                for item in items:
                    if dict_keyword.get(item):
                        kw_point = float(dict_keyword.get(item))
                    else:
                        kw_point = 0.2
                    if dict_keyword.get(item):
                        max += kw_point
                #for keyword in dict_seg:
                #    kw_point = float(dict_keyword.get(keyword))
                #    for item in items:
                #        if item == keyword:
                #            match += kw_point
                #        else:
                #            unmatch += kw_point * 0.3
            if max != 0.0:
                point = (match - unmatch) / max
                if point > 0.8:
                    print(items)
                    print(qa_ex_id, match, unmatch, max, point)
                    if point >= best[0]:
                        (qa_id, _) = qa_ex_id.split(':')
                        best.insert(0, point)
                        best_id.insert(0, qa_id)
        best.pop(-1)
        best_id.pop(-1)
        print('Best ID & point:', best_id, best)
    return best_id, best

dict_keyword = gen_keyword_dict("app/dict/keyword.dict")
dict_global_synonym = gen_dict_synonym("app/dict/synonym_global.dict")
dict_local_synonym = gen_dict_synonym("app/dict/synonym_local.dict")

@app.route('/qa', methods=['GET', 'POST'])
@app.route('/qa/', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        question = request.form.get('question')
        app.logger.info("Question: %s", question)
        dict_seg = {}
        fmm1 = fmmcut(question, dict_keyword, dict_global_synonym, dict_local_synonym)
        app.logger.info("Question Segmation: %s", fmm1)
        for word in fmm1:
            print(word)
            if '@' in word:
                word, importance = word.strip().split(',')
                _, word = word.strip().split('@')
                dict_seg[word] = float(importance)
        print(dict_seg)
        best_id, best_point = CountPoint(dict_seg)
        best_questions, best_answers, branch = get_qa(best_id)
        app.logger.info("Best id & point: %s %s", best_id, best_point)
        app.logger.info("Best Question: %s", best_questions)
        app.logger.info("Best Answer: %s", best_answers)
        return render_template('qa.html', question = question, qa = True, ids = best_id, points = best_point, questions = best_questions, answers = best_answers, )
    return render_template('qa.html',)
