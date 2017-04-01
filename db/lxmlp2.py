# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xmlp.py
# @time:2017/3/23 0023 21:35
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

xml_filename2 = 'knowledge.xml'

tree = etree.parse(xml_filename2)
root = tree.getroot()
i = 0
for knowledge in root:
    j = 0
    print ("元素名称：",knowledge.tag)
    for field in knowledge:
        if field.tag == "extend":
            row_data = []
            for item in field:
                for keyword in item:
                    row_data.append(keyword.text)
            print(field.tag, ":", row_data)
            j = j + 1
        else:
            print (field.tag,":",field.text)
    print("Extend ", j)
    i = i + 1
print("QA index ", i)

