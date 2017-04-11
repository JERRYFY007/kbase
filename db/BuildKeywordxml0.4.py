# -*- coding: utf-8 -*-
from lxml import etree

xml_filename2 = 'keyword.xml'

# Process keyword.xml
kw_data = []
sy_data = []
root = etree.parse(xml_filename2).getroot()
i, j = 0, 0
for keyword in root:
    row_data = []
    sy_id = 0
    for item in keyword:
        row_data.append(item.text.strip())
    while len(row_data) >= 3:
        sy_id = sy_id + 1
        kw_data.append(row_data[0].lower() + ',')
        kw_data.append(row_data[1] + ',')
        kw_data.append(row_data[-1] + '\n')
        sy_data.append(row_data[-1] + ',')
        sy_data.append(row_data[0] + '\n')
        row_data.pop(-1)
    if len(row_data) == 2:
        i = i + 1
        kw_data.append(row_data[0].lower() + ',')
        kw_data.append(row_data[1] + ',')
        kw_data.append('' + '\n')
    j += sy_id
print('Process keyword: ', i)
print('Process synonym: ', j)
open('keyword.dict', 'w', encoding='utf8').writelines(kw_data)
open('synonym.dict', 'w', encoding='utf8').writelines(sy_data)
print("最终词表文件建立完成! (keywordxml.dict)")


