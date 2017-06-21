# -*- coding: utf-8 -*-
# @author:Eric Luo
# @file:xlsx2xml.py
# @time:2017/4/27 0011 16:21
# 关键词,全局同义词
from lxml import etree

xml_filename = 'keyword.xml'
xml2_filename = '.xml'

# Process keyword.xml
keyword_data = ['value,importance']
root = etree.parse(xml_filename).getroot()
keyword_no = 0
dict_keyword = {}
for keyword in root:
    row_data = []
    for item in keyword:
        row_data.append(item.text.strip())
    value = row_data[0].lower()
    importance = row_data[1]
    dict_keyword[value] = importance
    keyword_data.append('\n' + value + ',' + importance)
    keyword_no += 1
    while len(row_data) > 2:
        value = row_data[-1].lower()
        dict_keyword[value] = importance
        keyword_data.append('\n' + value + ',' + importance)
        row_data.pop(-1)
        keyword_no += 1
print('Process Keyword: ', keyword_no)
print('Process Keyword Dict: ', len(dict_keyword))
open('keyword.dict', 'w', encoding='utf8').writelines(keyword_data)
print("keyword.dict文件建立完成!")
