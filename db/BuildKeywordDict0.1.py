# -*- coding: utf-8 -*-
import string
import re
from lxml import etree

xml_filename2 = 'keyword.xml'

# Process keyword.xml
tmp = []
root = etree.parse(xml_filename2).getroot()
i = 0
for element in root:
    category = element.tag
    row_data = []
    sy_id = 0
    for attribute in element:
        row_data.append(attribute.text.strip())
    if len(row_data) == 2:
        #print(row_data[0])
        tmp.append(row_data[0] + '\n')
        i = i + 1
    while len(row_data) >= 3:
        sy_id = sy_id + 1
        #print(row_data[0])
        tmp.append(row_data[2] + '\n')
        row_data.pop(-1)
    print('Process synonym: ', sy_id)
print('Process keyword: ' + str(i))

print("去重复前的词数为:", len(tmp))
set_data = set(tmp)  # 去重复
lalst_data = list(set_data)  # set转换成list, 否则不能索引
print("去除重复后总词数为:", len(lalst_data))

open('keyword.dict', 'w', encoding='utf8').writelines(lalst_data)
print("最终词表文件建立完成! (dict.txt)")


