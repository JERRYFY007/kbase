# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:view.py
# @time:2017/3/29
from flask import render_template, request
from app import *
from app import hmmseg
from .view import *
from .pymmseg import *


def gen_keyword_dict(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, im = line.strip().lower().split(',')
            if im != 'importance':
                dictionary_seg[word] = float(im)
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def gen_dict(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    words = []
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            dictionary_seg[words[0]] = int(words[1])
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


# 判断是否是ASCII码
def isASCIIChar(ch):
    import string
    if ch in string.whitespace:
        return False
    if ch in string.punctuation:
        return False
    return ch in string.printable


def mmcut(sentence, wordsdict1, wordsdict2, RMM=True):
    sentence = sentence.strip()
    result_s = ""
    s_length = len(sentence)
    english_word = ""
    if not RMM:
        result_s = "["
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if isASCIIChar(word[0]):
                    english_word = english_word + str(word[0])
                    word = word[1:]
                    sentence = sentence[1:]
                    w_length = len(word)
                    break
                elif english_word:
                    result_s += english_word + "]["
                    english_word = ""
                    break
                elif word in wordsdict1:
                    result_s += "@" + word + "," + str(wordsdict1.get(word)) + "]["
                    sentence = sentence[w_length:]
                    break
                elif word in wordsdict2 or w_length == 1:
                    result_s += word + "]["
                    sentence = sentence[w_length:]
                    break
                else:
                    word = word[:w_length - 1]
                w_length = w_length - 1
            s_length = len(sentence)
        result_s = result_s[:-1]
    else:
        result_s = "]"
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if w_length >0 and isASCIIChar(word[w_length - 1]):
                    # print(word[w_length - 1])
                    english_word = str(word[w_length - 1]) + english_word
                    sentence = sentence[:s_length - 1]
                    w_length -= 1
                    s_length -= 1
                    break
                if english_word:
                    # print(english_word)
                    result_s = english_word + "][" + result_s
                    english_word = ""
                    break
                elif word in wordsdict1:
                    result_s = "@" + word + "," + str(wordsdict1.get(word)) + "][" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in wordsdict2 or w_length == 1:
                    result_s = word + "][" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
        result_s = "[" + result_s[:-2]
    return result_s


keyworddict = gen_keyword_dict("app/dict/keyword.dict")
wordsdict = gen_dict("app/dict/sogou.dic_utf8")


@app.route('/segment', methods=['GET', 'POST'])
@app.route('/segment/', methods=['GET', 'POST'])
def segment():
    if request.method == 'POST':
        sentence = request.form.get('sentence')
        app.logger.info("Sentense: %s", sentence)
        fmm = ''.join(mmcut(sentence, keyworddict, wordsdict, RMM=False))
        rmm = ''.join(mmcut(sentence, keyworddict, wordsdict))
        hmm = ''.join(hmmseg.cut(sentence))
        mmseg = []
        words = Analysis(sentence)
        for word in words:
            mmseg.append(word)
        app.logger.info("FMM: %s", fmm)
        app.logger.info("RMM: %s", rmm)
        app.logger.info("HMM: %s", hmm)
        app.logger.info("MMSEG: %s", mmseg)
        segmented = []
        segmented.append('FMM: ')
        segmented.append(fmm)
        segmented.append('\n')
        segmented.append('RMM: ')
        segmented.append(rmm)
        segmented.append('\n')
        segmented.append('HMM: ')
        segmented.append(hmm)
        segmented.append('MMSEG: ')
        segmented.append(mmseg)
        analyse = []
        return render_template('segment.html', sentence=sentence, segmented=segmented, analyse=analyse)
    return render_template('segment.html')