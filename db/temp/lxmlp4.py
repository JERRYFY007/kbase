# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xmlp.py
# @time:2017/3/23 0023 21:35
from lxml import etree

xml_filename2 = 'knowledge.xml'

tree = etree.parse(xml_filename2)
root = tree.getroot()
qa_id = 0
for knowledge in root:
    qa_id = qa_id + 1
    ex_id = 0
    print("元素名称：", knowledge.tag)
    for field in knowledge:
        row_data = []
        key_id = 0
        sy_id = 0
        if field.tag == "extend":
            ex_id = ex_id + 1
            print("Extend:", ex_id)
            for item in field:
                for keyword in item:
                    sy_data = []
                    if keyword.tag == "keyword":
                        row_data.append(keyword.text)
                        key_id = key_id + 1
                    elif keyword.tag == "canOmit":
                        row_data.append(keyword.text)
                    elif keyword.tag == "synonym":
                        row_data.append(keyword.tag)
                        row_data.append(keyword.text)
                        sy_id = sy_id + 1
            print("keyword:", row_data, "keyword No.:", str(key_id), "synonym No.:", str(sy_id), )
        else:
            print(field.tag, ":", field.text)
    print("Extend ", ex_id)
print("QA index ", qa_id)
