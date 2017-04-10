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
        self.question = ''
        self.answer = ''
        self.extend = []    # 扩展问列表
        self.point = float  # 匹配分数


class Extend(object):
    def __init__(self):
        self.keyword = ''  # 读取时只有keyword的value，在正式运行的程序里才会关联Keyword
        self.canOmit = False
        self.synonym = []   # 局部同义词列表

    def load(self, dictfile):
        print("Building dictionary...")
        with open(dictfile, "r", encoding='utf-8') as f:
            for line in f:
                self.keyword, self.synonym = line.strip().split('|')
        f.close()
        print("The volumn of dictionary: %d")
        return


class Keyword(object):
    def __init__(self):
        self.keyword = []
        self.importance = []    # 关键词的值
        self.synonym = []   # 全局同义词列表
        self.type = []  # 一级类型
        self.type2 = [] # 二级类型
        self.info = []  # 附加信息：如人名关键词的附加信息info为其电话号码

    def load(self, xml_filename):
        print("Building dictionary...")
        root = etree.parse(xml_filename).getroot()
        for keywords in root:
            row_data = []
            for item in keywords:
                row_data.append(item.text.strip())
                print(row_data)
            if len(row_data) >= 3:
                self.keyword.append(row_data[0])
                self.importance.append(row_data[1])
                self.synonym.append(row_data[-1])
                row_data.pop(-1)
            elif len(row_data) == 2:
                self.keyword.append(row_data[0])
                self.importance.append(row_data[1])
                self.synonym.append('')
        #for i in range(len(self.synonym)):
        #    print(self.keyword[i], self.importance[i], self.synonym[i])
        print(self.keyword, self.importance, self.synonym)
        print("The volumn of dictionary:", len(self.keyword), len(self.importance), len(self.synonym)  )
        return


def gen_dict_extend(dictfile):
    print("Building Extend dictionary...")
    d1 = {}
    d2 = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, qa_id = line.lower().strip().split(',')
            d1[word] = 1
            d2[qa_id] = 1
    f.close()
    print("The volumn of Extend dictionary: %d",  len(d1), len(d2))
    return d1, d2


def findextend(words, d1, d2):
    qa_id = []
    ex_impo = 0.0
    for word in words:
        if '@' in word:
            word, impo = word.strip().split(',')
            _, word = word.strip().split('@')
            print(word, impo)
            ex_impo += float(impo)
            if word in d1:
                qa_id.append(d2[d1.index(word)])
    return qa_id, ex_impo


def fmmcut(sentence, wordsdict1, wordsdict2, wordsdict3, FMM=True):
    result_s = []
    s_length = len(sentence)
    if FMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict1:
                    synonym = wordsdict1.get(word)
                    result_s.append("#" + synonym + "," + str(wordsdict2.get(synonym)))
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
                    result_s.insert(0, ("#" + synonym + "," + str(wordsdict2.get(synonym))))
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


# d1, d2 = gen_dict_extend("app/dict/extend1.dict")
@app.route('/dialog', methods=['GET', 'POST'])
@app.route('/dialog/', methods=['GET', 'POST'])
def dialog():
    extend = Extend()
    extend.load("app/dict/synonym.dict")
    keyword = Keyword()
    keyword.load("app/dict/keyword.xml")
    if request.method == 'POST':
        question = request.form.get('question')
        answer = []
        fmm1 = fmmcut(question, wordsdict1, wordsdict2, wordsdict3)
        print(fmm1)
        # answer = findextend(fmm1, d1, d2)
        print(answer)
        return render_template('dialog.html', dialog = True, question = question, answer = answer, )
    return render_template('dialog.html',)
