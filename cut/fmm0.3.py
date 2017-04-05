# -*- coding: utf-8 -*-

# 新建列表存放分词词典读出来的词
d = []
with open('sogou.dic_utf8', 'r', encoding='utf-8') as fd:
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
        s = flist.split()
        d.append(s[0])
    # 将列表转换为元祖
    synonym = tuple(d)

wordSeg = []    # 新建列表存放切分好的词
maxWordLen = 4  # 最大词长设为3
with open('question.txt', 'r', encoding='utf-8') as src:
    sentence = src.read()
    sentenceLen = len(sentence)
    wordLen = min(maxWordLen, sentenceLen)
    startPoint = 0
    while startPoint < sentenceLen:  # 从第一个字符循环到最后一个字符
        matched = False    # 假设找不到匹配的词
        for i in range(maxWordLen, 0, -1):  # 从最大词长4递减到1
            string = sentence[startPoint:startPoint+i]  # 取startPoint开始到startPoint+i-1的切片
            if string in synonym:
                # print('Find in synonym:', string)
                wordSeg.append(string)
                matched = True
                startPoint += len(string)
                break
            elif string in keyword:
                # print('Find in keyword:', string)
                wordSeg.append(string)
                matched = True
                startPoint += len(string)
                break
            elif string in sogou:
                # print('Find in sogou:', string)
                wordSeg.append(string)
                matched = True
                startPoint += len(string)
                break
        if not matched:    # 假如在词典中找不到匹配
            i = 1
            wordSeg.append(sentence[startPoint])   # 全部切分为单字词
            startPoint += i
        print(sentence, wordSeg)

with open('question.seg', 'w', encoding='utf-8') as des:
    for word in wordSeg:
        des.write(word+'  ')
