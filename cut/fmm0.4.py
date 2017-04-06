# -*- coding: utf-8 -*-
from tqdm import *

# 新建列表存放分词词典读出来的词
sogou = {}
with open('../jieba.dict.utf8', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        s, freq, _ = flist.strip().split()
        sogou[s] = int(freq)
keyword = {}
with open('keywordxml.dic', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        s = flist.strip()
        keyword[s] = len(s)
synonym = {}
with open('synonym.tmp', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        s1, s2 = flist.strip().split('|')
        synonym[s1] = s2

des = open('answer_fmm.txt', 'w', encoding='utf-8')
maxWordLen = 6  # 最大词长设为6
with open('answer.txt', 'r', encoding='utf-8') as src:
    for j in tqdm(range(3570)):
        sentence = src.readline()
        if not sentence: break
        sentenceLen = len(sentence)
        wordLen = min(maxWordLen, sentenceLen)
        wordSeg = []  # 新建列表存放切分好的词
        startPoint = 0
        while startPoint < sentenceLen:  # 从第一个字符循环到最后一个字符
            matched = False    # 假设找不到匹配的词
            for i in range(maxWordLen, 0, -1):  # 从最大词长6递减到1
                string = sentence[startPoint:startPoint+i]  # 取startPoint开始到startPoint+i-1的切片
                if string in synonym:
                    wordSeg.append(str('@' + synonym.get(string) +  '@'))
                    matched = True
                    startPoint += len(string)
                    break
                elif string in keyword:
                    wordSeg.append(string)
                    matched = True
                    startPoint += len(string)
                    break
                elif string in sogou:
                    wordSeg.append(string)
                    matched = True
                    startPoint += len(string)
                    break
            if not matched:    # 假如在词典中找不到匹配
                i = 1
                wordSeg.append(sentence[startPoint])   # 全部切分为单字词
                startPoint += i
        # print(sentence, wordSeg)
        for word in wordSeg:
            des.write(word + '|')
des.close()
