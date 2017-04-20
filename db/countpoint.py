# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:pandas0.1.py
# @time:2017/4/14 0014 22:19

dict_keyword = {}
with open("keyword.dict", encoding='utf8') as f:
    for line in f:
       (val, imp) = line.strip().split(',')
       dict_keyword[val] = imp
# print(dict_keyword)

dict_extend_item = {}
with open("extend_item.dict", encoding='utf8') as f:
    for line in f:
       (qa_ex_id, item) = line.strip().split(',')
       dict_extend_item[qa_ex_id] = item
# print(dict_extend_item)

dict_seg = {}
with open("seg2.txt", encoding='utf8') as f:
    for line in f:
       (seg, imp) = line.strip().split(',')
       dict_seg[seg] = imp
print(dict_seg)

with open("extend_point.df", encoding='utf8') as f:
    best_id = ''
    point, best = 0, 0
    for line in f:
        (qa_ex_id, _, _, _, _) = line.strip().split(',')
        max, match, unmatch = 0.0, 0.0, 0.0
        success = False
        if dict_extend_item.get(qa_ex_id) and (dict_extend_item.get(qa_ex_id) != 'Item'):
            items = dict_extend_item.get(qa_ex_id).split(';')
            items.pop(-1)
            for item in items:
                if dict_keyword.get(item):
                    max += float(dict_keyword.get(item))
                if dict_seg.get(item):
                    match += float(dict_keyword.get(item))
                    success = True
                else:
                    unmatch += float(dict_keyword.get(item)) * 0.3
            if match > unmatch:
                print(qa_ex_id, max, match, unmatch)
        if max != 0.0:
            point = (match - unmatch) / max
            # print(qa_ex_id, point)
            if point > best:
                best = point
                best_id = qa_ex_id
    print('Best ID & point:', best_id, best)
