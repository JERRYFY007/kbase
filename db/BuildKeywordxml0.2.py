# -*- coding: utf-8 -*-
from lxml import etree

xml_filename2 = 'keyword.xml'

# Process keyword.xml
tmp, synonym = [], []
kw_data = []
root = etree.parse(xml_filename2).getroot()
i, j = 0, 0
for keyword in root:
    row_data = []
    sy_id = 0
    for item in keyword:
        row_data.append(item.text.strip())
    while len(row_data) >= 3:
        sy_id = sy_id + 1
        # print(row_data[0], '|', row_data[-1])
        synonym.append(row_data[-1] + '|')
        synonym.append(row_data[0] + '\n')
        row_data.pop(-1)
    if len(row_data) == 2:
        i = i + 1
        tmp.append(row_data[0] + '\n')
        kw_data.append(row_data[0] + ', ')
        kw_data.append(row_data[1] + '\n')
    j += sy_id
print('Process keyword: ', i)
print('Process synonym: ', j)
open('keywordxml.dict', 'w', encoding='utf8').writelines(kw_data)
open('keywordxml.tmp', 'w', encoding='utf8').writelines(tmp)
open('synonym.tmp', 'w', encoding='utf8').writelines(synonym)
print("最终词表文件建立完成! (keywordxml.tmp, synonym.tmp, keywordxml.dict)")


