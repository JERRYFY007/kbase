# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:pandas0.1.py
# @time:2017/4/14 0014 22:19

dict_keyword = {}
with open("keyword.dict", encoding='utf8') as f:
    for line in f:
       (val, imp, _) = line.strip().split(',')
       dict_keyword[val] = imp
print(dict_keyword)

dict_extend_item = {}
with open("extend_item.dict", encoding='utf8') as f:
    for line in f:
       (qa_ex_id, item) = line.strip().split(',')
       dict_extend_item[qa_ex_id] = item
print(dict_extend_item)

dict_extend_point = {}
with open("extend_point.df", encoding='utf8') as f:
    for line in f:
       (qa_ex_id, best, max, match, unmatch) = line.strip().split(',')
       dict_extend_point[qa_ex_id] = best
print(dict_extend_point)
