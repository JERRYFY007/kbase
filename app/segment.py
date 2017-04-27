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
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, freq, _ = line.strip().split()
            dictionary_seg[word] = int(freq)
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def mmcut(sentence, wordsdict1, wordsdict2, RMM=True):
    sentence = sentence.lower()
    result_s = ""
    s_length = len(sentence)
    if not RMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict1:
                    result_s += "@" + word + "," + str(wordsdict1.get(word)) + "/"
                    sentence = sentence[w_length:]
                    break
                elif word in wordsdict2 or w_length == 1:
                    result_s += word + "/"
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
                    result_s = "@" + word + "," + str(wordsdict1.get(word)) + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in wordsdict2 or w_length == 1:
                    result_s = word + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
    return result_s


keyworddict = gen_keyword_dict("app/dict/keyword.dict")
wordsdict = gen_dict("app/dict/dict.txt")


@app.route('/segment', methods=['GET', 'POST'])
@app.route('/segment/', methods=['GET', 'POST'])
def segment():
    if request.method == 'POST':
        sentence = request.form.get('sentence')
        fmm = ''.join(mmcut(sentence, keyworddict, wordsdict, RMM=False))
        rmm = ''.join(mmcut(sentence, keyworddict, wordsdict))
        hmm = ''.join(hmmseg.cut(sentence))
        mmseg = []
        words = Analysis(sentence)
        for word in words:
            print(word)
            mmseg.append(word)
        print(mmseg)
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