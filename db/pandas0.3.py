# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:pandas0.1.py
# @time:2017/4/14 0014 22:19
from pandas.io.parsers import read_csv
import pandas as pd


#df = read_csv("keyword.dict", encoding='utf8')
#print(df)
#dict_keyword = dict(zip(df.value, df.importance))
dict_keyword = {}
with open("keyword.dict", encoding='utf8') as f:
    for line in f:
       (val, imp, _) = line.strip().split(',')
       dict_keyword[val] = imp
print(dict_keyword)

df_extend = read_csv('extend.df')
df_extend_point = read_csv('extend_point.df')
#df_seg = read_csv("seg2.txt", encoding='utf8')
#print(df_seg)
for i in range(62590):
