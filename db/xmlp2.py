# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xmlp.py
# @time:2017/3/23 0023 21:35
from lxml import etree

xml_filename1 = 'knowledge.xml'

tree = etree.parse("knowledge.xml")
root = tree.getroot()
i = 0
for knowledge in root:
    print ("元素名称：",knowledge.tag)
    for field in knowledge:
        print (field.tag,":",field.text)
    i = i + 1
    print(i)
    print ("")