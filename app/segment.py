# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:view.py
# @time:2017/3/29
from flask import render_template, request
from app import app
from app import hmmseg


def gen_dict1(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, sy = line.strip().split('|')
            dictionary_seg[word] = sy
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def gen_dict2(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, freg = line.strip().split(',')
            dictionary_seg[word] = str(freg)
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


def gen_dict_extend(dictfile):
    print("Building Extend dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, qa_id = line.strip().split(',')
            dictionary_seg[word] = qa_id
    f.close()
    print("The volumn of Extend dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def findextend(words, dict_extend):
    qa_id = []
    ex_impo = 0.0
    for word in words:
        if '@' in word:
            word, impo = word.strip().split(',')
            _, word = word.strip().split('@')
            print(word, impo)
            ex_impo += float(impo)
            qa_id.append(dict_extend.get(word))
    return qa_id, ex_impo


def mmcut(sentence, wordsdict1, wordsdict2, wordsdict3, RMM=True):
    result_s = ""
    s_length = len(sentence)
    if not RMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict1:
                    synonym = wordsdict1.get(word)
                    result_s += "#" + synonym + "," + str(wordsdict2.get(synonym)) + "/"
                    sentence = sentence[w_length:]
                    break
                elif word in wordsdict2:
                    result_s += "@" + word + "," + str(wordsdict2.get(word)) + "/"
                    sentence = sentence[w_length:]
                    break
                elif word in wordsdict3 or w_length == 1:
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
                    synonym = wordsdict1.get(word)
                    result_s = "#" + synonym + "," + str(wordsdict2.get(synonym)) + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in wordsdict2:
                    result_s = "@" + word + "," + str(wordsdict2.get(word)) + "/" + result_s
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


wordsdict1 = gen_dict1("app/dict/synonym.dict")
wordsdict2 = gen_dict2("app/dict/keywordxml.dict")
wordsdict3 = gen_dict("app/dict/dict.txt")
@app.route('/segment', methods=['GET', 'POST'])
@app.route('/segment/', methods=['GET', 'POST'])
def segment():
    if request.method == 'POST':
        dict_extend = gen_dict_extend("app/dict/extend.dict")
        sentence = request.form.get('sentence')
        fmm = ''.join(mmcut(sentence, wordsdict1, wordsdict2, wordsdict3, RMM=False))
        rmm = ''.join(mmcut(sentence, wordsdict1, wordsdict2, wordsdict3, ))
        hmm = ''.join(hmmseg.cut(sentence))
        segmented = []
        segmented.append('FMM: ')
        segmented.append(fmm)
        segmented.append('\n')
        segmented.append('RMM: ')
        segmented.append(rmm)
        segmented.append('\n')
        segmented.append('HMM: ')
        segmented.append(hmm)
        fmm1 = fmmcut(sentence, wordsdict1, wordsdict2, wordsdict3)
        print(fmm1)
        analyse = findextend(fmm1, dict_extend)
        print(analyse)
        return render_template('segment.html', sentence=sentence, segmented=segmented, analyse=analyse)
    return render_template('segment.html')