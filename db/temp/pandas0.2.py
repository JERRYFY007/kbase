# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:pandas0.1.py
# @time:2017/4/14 0014 22:19
from pandas.io.parsers import read_csv
import pandas as pd

df = read_csv('extend.dict')
df_keyword = read_csv("keyword.dict", encoding='utf8')
df_seg = read_csv("seg2.txt", encoding='utf8')
df = pd.merge(df, df_keyword, how='left', on='Item')
df = pd.merge(df, df_seg, how='left', on='Item')
df_qa_ex = pd.merge(df, df_seg, how='right', on='Item')

dict_qa_point = {}
for qa in df_qa_ex['qa_id:ex_id']:
    df_qa = df.loc[df['qa_id:ex_id'] == qa, ]
    dict_qa_point[qa] = df_qa['im'].sum() * 2 - df_qa['importance'].sum()

print(len(dict_qa_point))
for k, v in dict_qa_point.items():
   if v > 1:
       print(k, v)

match = max(dict_qa_point, key=dict_qa_point.get)
print("MAX1: ",match, dict_qa_point[match])
dict_qa_point.pop(match)
match = max(dict_qa_point, key=dict_qa_point.get)
print("MAX2: ",match, dict_qa_point[match])
dict_qa_point.pop(match)
match = max(dict_qa_point, key=dict_qa_point.get)
print("MAX3: ",match, dict_qa_point[match])
dict_qa_point.pop(match)
match = max(dict_qa_point, key=dict_qa_point.get)
print("MAX4: ",match, dict_qa_point[match])
dict_qa_point.pop(match)
match = max(dict_qa_point, key=dict_qa_point.get)
print("MAX5: ",match, dict_qa_point[match])
dict_qa_point.pop(match)
