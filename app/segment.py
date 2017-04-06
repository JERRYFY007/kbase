# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:view.py
# @time:2017/3/29
from flask import render_template, request

from app import app
from app import hmmseg


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


def mmcut(sentence, wordsdict, RMM=True):
    result_s = ""
    s_length = len(sentence)
    if not RMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict or w_length == 1:
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
                if word in wordsdict or w_length == 1:
                    result_s = word + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
    return result_s


@app.route('/segment', methods=['GET', 'POST'])
@app.route('/segment/', methods=['GET', 'POST'])
def segment():
    if request.method == 'POST':
        segment = request.form.get('sentence')
        segmented = []
        wordsdict = gen_dict("app/dict/dict.txt")
        segmented.append('FMM: ')
        segmented.append(''.join(mmcut(segment, wordsdict, RMM=False)))
        segmented.append('\n')
        segmented.append('RMM: ')
        segmented.append(''.join(mmcut(segment, wordsdict,)))
        segmented.append('\n')
        segmented.append('HMM: ')
        segmented.append(''.join(hmmseg.cut(segment)))
        analyse = []
        return render_template('segment.html', sentence=segment, segmented=segmented, analyse=analyse)
    return render_template('segment.html')