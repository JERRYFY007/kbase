# -*- coding: utf-8 -*-
from tqdm import *

# 新建列表存放分词词典读出来的词
sogou = {}
with open('../jieba.dict.utf8', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        word, freq, _ = flist.strip().split()
        sogou[word] = int(freq)
keyword = {}
with open('keywordxml.dict', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        word, freq = flist.strip().split(',')
        keyword[word] = freq
synonym = {}
with open('synonym.tmp', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        word, sy = flist.strip().split('|')
        synonym[word] = sy

des = open('question_rmm.txt', 'w', encoding='utf-8')

maxWordLen = 6  # 最大词长设为6
with open('question.txt', 'r', encoding='utf-8') as src:
    for j in tqdm(range(3570)):
        sentence = src.readline()
        if not sentence: break
        sentence = sentence.lower()
        sentenceLen = len(sentence)
        wordLen = min(maxWordLen, sentenceLen)
        wordSeg = []  # 新建列表存放切分好的词
        startPoint = sentenceLen
        while startPoint > 0:  # 从第一个字符循环到最后一个字符
            matched = False    # 假设找不到匹配的词
            for i in range(wordLen, 0, -1):  # 从最大词长6递减到1
                string = sentence[startPoint-i:startPoint]  # 取startPoint开始到startPoint+i-1的切片
                if string in synonym:
                    wordSeg.insert(0, str('#' + synonym.get(string) + ',' + keyword.get(synonym.get(string))))
                    matched = True
                    startPoint -= len(string)
                    break
                elif string in keyword:
                    wordSeg.insert(0, str('@' + string + ',' + keyword.get(string)))
                    matched = True
                    startPoint -= len(string)
                    break
                elif string in sogou:
                    wordSeg.insert(0, string)
                    matched = True
                    startPoint -= len(string)
                    break
            if not matched:    # 假如在词典中找不到匹配
                i = 1
                wordSeg.insert(0, sentence[startPoint-i:startPoint])   # 全部切分为单字词
                startPoint -= i
        for word in wordSeg:
            des.write(word + '/')
des.close()