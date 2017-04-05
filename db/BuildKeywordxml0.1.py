# -*- coding: utf-8 -*-
from lxml import etree

xml_filename2 = 'keyword.xml'

# 新建列表存放分词词典读出来的词
d = []
with open('sogou.dic_utf8', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        s = flist.split()
        d.append(s[0])
    # 将列表转换为元祖
    lexicon = tuple(d)

# Process keyword.xml
tmp, synonym = [], []
kw_data = []
root = etree.parse(xml_filename2).getroot()
i = 0
for keyword in root:
    row_data = []
    sy_id = 0
    for item in keyword:
        row_data.append(item.text.strip())
    if len(row_data) == 2:
        i = i + 1
        # print(row_data[0])
        if row_data[0] in lexicon:
            tmp.append(row_data[0] + '\n')
            kw_data.append(row_data[0] + ', ')
            kw_data.append(row_data[1] + '\n')
            matched = True
        else:
            print('keyword not in dict: ', row_data[0])
    while len(row_data) >= 3:
        sy_id = sy_id + 1
        synonym.append(row_data[2] + '\n')
        row_data.pop(-1)
    # print('Process synonym: ', sy_id)
print('Process keyword: ', i)

print("去重复前的词数为:", len(tmp))
set_data = set(tmp)  # 去重复
lalst_data = list(set_data)  # set转换成list, 否则不能索引

last_synonym = list(set(synonym))
print("去除重复后总词数为:", len(lalst_data))

open('keywordxml.dict', 'w', encoding='utf8').writelines(kw_data)
open('keywordxml.tmp', 'w', encoding='utf8').writelines(lalst_data)
open('synonym.tmp', 'w', encoding='utf8').writelines(last_synonym)
print("最终词表文件建立完成! (keywordxml.tmp)")


