# -*- coding: utf-8 -*-
from lxml import etree

xml_filename = 'keyword.xml'

# Process keyword.xml
kw_data = ['value,importance,synonym']
keyword_data = ['value,importance']
sy_data = ['synonym,keyword']
root = etree.parse(xml_filename).getroot()
keyword_no, synonym_no = 0, 0
dict_keyword, dict_synonym = {}, {}
for keyword in root:
    row_data = []
    for item in keyword:
        row_data.append(item.text.strip())
    while len(row_data) >= 3:
        synonym_no += 1
        value = row_data[0].lower()
        synonym = row_data[-1].lower()
        importance = row_data[1]
        kw_data.append('\n' + value + ',')
        kw_data.append(importance + ',')
        keyword_data.append('\n' + value + ',' + importance)
        dict_keyword[value] = importance
        dict_synonym[synonym] = value
        kw_data.append(synonym)
        keyword_data.append('\n' + synonym + ',' + importance)
        sy_data.append('\n' + synonym + ',')
        sy_data.append(value)
        row_data.pop(-1)
    if len(row_data) == 2:
        keyword_no += 1
        value = row_data[0].lower()
        importance = row_data[1]
        kw_data.append('\n' + value + ',')
        kw_data.append(importance + ',')
        keyword_data.append('\n' + value + ',' + importance)
        dict_keyword[value] = importance
print('Process Keyword: ', keyword_no)
print('Process Synonym: ', synonym_no)
print('Process Keyword Dict: ', len(dict_keyword))
print('Process Synonym Dict: ', len(dict_synonym))
open('keyword.df', 'w', encoding='utf8').writelines(kw_data)
open('keyword.dict', 'w', encoding='utf8').writelines(keyword_data)
open('synonym.dict', 'w', encoding='utf8').writelines(sy_data)
print("最终词表文件建立完成! (keyword.dict & synonym.dict)")
