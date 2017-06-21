# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xmlp.py
# @time:2017/3/23 0023 21:35
from lxml import etree

xml_filename2 = 'knowledge.xml'

tree = etree.parse(xml_filename2)
root = tree.getroot()
i = 0
for knowledge in root:
    j = 0
    print("元素名称：", knowledge.tag)
    for field in knowledge:
        row_data = []
        key_id, sy_id, omit = 0, 0, 0
        if field.tag == "extend":
            for item in field:
                for keyword in item:
                    sy_data = []
                    sy_id = 0
                    if keyword.tag == "keyword":
                        # print(keyword.tag, keyword.text)
                        row_data.append(keyword.text)
                        key_id = key_id + 1
                    elif keyword.tag == "canOmit":
                        # print(keyword.tag, keyword.text)
                        row_data.append(keyword.text)
                        omit = omit + 1
                    elif keyword.tag == "synonym":
                        row_data.append(keyword.tag)
                        row_data.append(keyword.text)
                        sy_id = sy_id + 1
            print("keyword:", row_data, "keyword no.:", str(key_id))
            j = j + 1
        else:
            print(field.tag, ":", field.text)
    print("Extend ", j)
    i = i + 1
print("QA index ", i)
