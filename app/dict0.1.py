# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:dict0.1.py
# @time:2017/6/11 0011 15:34

dict_extend = {}
with open("dict/extend.dict", encoding='utf8') as f:
    for line in f:
        # print(line)
        dict_item = {}
        (qa_ex_id, item) = line.strip().split(',')
        if item == "Item":
            continue
        # print(qa_ex_id, item)
        items = item.split(';')
        items.pop(-1)
        # print(items)
        sy = []
        for keyword in items:
            # print(keyword)
            sy.append(keyword.split('|'))
            dict_item[keyword] = sy
        # print("Extend:", sy)
        dict_extend[qa_ex_id] = sy
print(dict_extend)
print("Dict extend sy", len(dict_extend))
