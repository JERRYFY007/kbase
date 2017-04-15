# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:pandas0.1.py
# @time:2017/4/14 0014 22:19
from pandas.io.parsers import read_csv
import pandas as pd

df = read_csv('extend.dict')
print("Dataframe", df)
print("Shape", df.shape)
print("Length", len(df))
print("Column Headers", df.columns)
print("Data Types", df.dtypes)
print("Index", df.index)

item_col = df["Item"]
print("Type df", type(df))
print("Type Item col", type(item_col))
print("Series shape", item_col.shape)
print("Series index", item_col.index)
print("Series values", item_col.values)
print("Series name", item_col.name)

df_kw = read_csv("seg1.txt", encoding='gbk')
print("Dataframe", df_kw)