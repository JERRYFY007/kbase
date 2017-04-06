# -*- coding: utf-8 -*-

# 新建列表存放分词词典读出来的词
d = []
with open('../jieba.dict.utf8', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        s = flist.split()
        d.append(s[0])
    # 将列表转换为元祖
    sogou = tuple(d)
d = []
with open('keywordxml.dic', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        s = flist.split()
        d.append(s[0])
    # 将列表转换为元祖
    keyword = tuple(d)
d = []
with open('synonym.tmp', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        s = flist.split('|')
        d.append(s[0])
    # 将列表转换为元祖
    synonym = tuple(d)

des = open('question.seg', 'w', encoding='utf-8')

maxWordLen = 5  # 最大词长设为4
with open('question.txt', 'r', encoding='utf-8') as src:
    for j in range(500):
        sentence = src.readline()
        if not sentence: break
        sentenceLen = len(sentence)
        wordLen = min(maxWordLen, sentenceLen)
        # FMM
        fmmwordSeg = []  # 新建列表存放切分好的词
        startPoint = 0
        while startPoint < sentenceLen:  # 从第一个字符循环到最后一个字符
            matched = False    # 假设找不到匹配的词
            for i in range(maxWordLen, 0, -1):  # 从最大词长4递减到1
                string = sentence[startPoint:startPoint+i]  # 取startPoint开始到startPoint+i-1的切片
                if string in keyword:
                    # print('Find in keyword:', string)
                    fmmwordSeg.append(string)
                    matched = True
                    startPoint += len(string)
                    break
                elif string in sogou:
                    # print('Find in sogou:', string)
                    fmmwordSeg.append(string)
                    matched = True
                    startPoint += len(string)
                    break
            if not matched:    # 假如在词典中找不到匹配
                i = 1
                fmmwordSeg.append(sentence[startPoint])   # 全部切分为单字词
                startPoint += i
        # RMM
        rmmwordSeg = []  # 新建列表存放切分好的词
        startPoint = sentenceLen
        while startPoint > 0:
            matched = False    # 假设找不到匹配的词
            for i in range(maxWordLen, 0, -1):  # 从最大词长4递减到1
                string = sentence[startPoint-i:startPoint]  # 取startPoint开始到startPoint+i-1的切片
                if string in keyword:
                    rmmwordSeg.insert(0, string)
                    matched = True
                    startPoint -= len(string)
                    break
                elif string in sogou:
                    rmmwordSeg.insert(0, string)
                    matched = True
                    startPoint -= len(string)
                    break
            if not matched:    # 假如在词典中找不到匹配
                i = 1
                rmmwordSeg.insert(0, sentence[startPoint-i:startPoint])   # 全部切分为单字词
                startPoint -= i
        # print(sentence, fmmwordSeg, rmmwordSeg)
        des.write('-' * 30)
        des.write(sentence)
        for word in fmmwordSeg:
            des.write(word + '  ')
        for word in rmmwordSeg:
            des.write(word + '  ')

