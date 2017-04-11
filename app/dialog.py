# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:dialog.py
# @time:2017/4/10 0010 16:04
from flask import render_template, request
from app import *
from .segment import *
from lxml import etree

class Knowledge(object):
    def __init__(self):
        self.qa_id = []
        self.question = []
        self.answer = []
        self.extend = []    # 扩展问列表
        self.point = []  # 匹配分数

    def load(self, xml_filename):
        print("Building Knowledge dictionary...")
        root = etree.parse(xml_filename).getroot()
        qa_id = 0
        qa_data = []
        for knowledge in root:
            qa_id += 1
            ex_id = 0
            ex_data = []
            for field in knowledge:
                if field.text is None:
                    ex_id += 1
                    kw_data = []
                    for item in field:
                        row_data = []
                        for keywords in item:
                            row_data.append(keywords.text.strip())
                        kw_data.append(row_data)
                    ex_data.append(ex_id)
                    ex_data.append(kw_data)
                else:
                    qa_data.append(field.text.strip())
            self.qa_id.append(qa_id)
            self.question.append(qa_data[0])
            self.answer.append(qa_data[1])
            qa_data.clear()
            self.extend.append(ex_data)
            self.point.append(0.0)
        # print(self.answer[7])
        print("The volumn of dictionary:", len(self.question), len(self.answer), len(self.extend))
        return

    def answer(self, qa_id):
        print(qa_id)
        qa_id -= 1
        return self.question[qa_id], self.answer[qa_id]


class Extend(object):
    def __init__(self):
        self.keyword = []  # 读取时只有keyword的value，在正式运行的程序里才会关联Keyword
        self.canOmit = []
        self.synonym = []   # 局部同义词列表
        self.qa_id = []
        self.ex_id = []
        self.kw_id = []
        self.sy_id = []
        self.point = []


    def load(self, xml_filename):
        print("Building Extend dictionary...")
        root = etree.parse(xml_filename).getroot()
        qa_id = 0
        for knowledge in root:
            qa_id = qa_id + 1
            ex_id = 0
            for field in knowledge:
                if field.text is None:
                    ex_id = ex_id + 1
                    kw_id = 0
                    for item in field:
                        row_data = []
                        kw_id += 1
                        for keywords in item:
                            row_data.append(keywords.text.strip())
                        sy_data = []
                        while len(row_data) >= 3:
                            sy_id = len(row_data) - 2
                            sy_data.append(sy_id)
                            sy_data.append(row_data[-1].lower())
                            row_data.pop(-1)
                        sy_id = 0
                        self.keyword.append(row_data[0].lower().strip())
                        self.canOmit.append(row_data[1])
                        self.synonym.append(sy_data)
                        self.qa_id.append(qa_id)
                        self.ex_id.append(ex_id)
                        self.kw_id.append(kw_id)
                        self.sy_id.append(sy_id)
                        self.point.append(0.0)
        print(self.keyword)
        print("The volumn of Extend dictionary:", len(self.keyword), len(self.canOmit), len(self.synonym)  )
        return

    def extend_word_point(self, word, point):
        # print(point)
        match, unmatch = 0, 0
        success = False
        p = point
        word = word.strip()
        print(word)
        if word in self.keyword:
            i = self.keyword.index(word)
            print(i)
            self.point[i] += p
            #else:
                #self.point[i] -= p
        return

    def extend_point(self):
        find = []
        max = 0
        match, unmatch = 0, 0
        success = False
        print(len(self.point))
        for i in range(len(self.point)):
            if self.point[i] > 0:
                if self.point[i] > max:
                    max = self.point[i]
                    find.append(self.qa_id[i])
                    find.append(self.ex_id[i])
                    find.append(self.point[i])

        return find


class Keyword(object):
    def __init__(self):
        self.keyword = []
        self.importance = []    # 关键词的值
        self.synonym = []   # 全局同义词列表
        self.type = []  # 一级类型
        self.type2 = [] # 二级类型
        self.info = []  # 附加信息：如人名关键词的附加信息info为其电话号码

    def load(self, xml_filename):
        print("Building Keyword dictionary...")
        root = etree.parse(xml_filename).getroot()
        for keywords in root:
            row_data = []
            for item in keywords:
                row_data.append(item.text.strip())
            while len(row_data) > 3:
                self.keyword.append(row_data[0])
                self.importance.append(row_data[1])
                self.synonym.append(row_data[-1])
                row_data.pop(-1)
            if len(row_data) == 3:
                self.keyword.append(row_data[0])
                self.importance.append(row_data[1])
                self.synonym.append(row_data[-1])
            elif len(row_data) == 2:
                self.keyword.append(row_data[0])
                self.importance.append(row_data[1])
                self.synonym.append('')
        # print(self.keyword, self.importance, self.synonym)
        print("The volumn of dictionary:", len(self.keyword), len(self.importance), len(self.synonym)  )
        return

    def importance(self, word):
        while word in self.keyword:
            return float(self.importance[self.keyword.index(word)])
        return 0


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

knowledge = Knowledge()
knowledge.load("app/dict/knowledge.xml")
extend = Extend()
extend.load("app/dict/knowledge.xml")
keyword = Keyword()
keyword.load("app/dict/keyword.xml")


@app.route('/dialog', methods=['GET', 'POST'])
@app.route('/dialog/', methods=['GET', 'POST'])
def dialog():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = []
        fmm1 = fmmcut(question, wordsdict1, wordsdict2, wordsdict3)
        print(fmm1)
        point = 0.0
        answer.append(fmm1)
        for word in fmm1:
            if '@' in word:
                word1, impo = word.strip().split(',')
                _, word = word1.strip().split('@')
                print(word, impo)
                point += Keyword.importance(keyword, word)
                answer.append(word)
                Extend.extend_word_point(extend, word, float(impo))
        ex_data = Extend.extend_point(extend)
        print(ex_data)
        qa_id = ex_data[0]
        answer.append(Knowledge.answer(knowledge, qa_id))
        print(point)
        return render_template('dialog.html', dialog = True, question = question, answers = answer, )
    return render_template('dialog.html',)
