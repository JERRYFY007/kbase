# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xmlp.py
# @time:2017/3/23 0023 21:35
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

xml_filename1 = 'keyword.xml'
xml_filename2 = 'knowledge.xml'

tree = etree.parse(xml_filename2)
root = tree.getroot()
i = 0

knowledges = tree.xpath("//knowledge/question")
for knowledge in knowledges:
    i = i + 1
# print(knowledge.text)
print(len(knowledges))

knowledges = tree.xpath("//knowledge/answer")
for knowledge in knowledges:
    i = i + 1
# print(knowledge.text)
print(len(knowledges))

extends = tree.xpath("//extend/item/keyword")
for extend in extends:
    # print(extend.text)
    i = i + 1
print(len(extends))

extends = tree.xpath("//extend/item/canOmit")
for extend in extends:
    # print(extend.text)
    i = i + 1
print(len(extends))

extends = tree.xpath("//extend/item/synonym")
for extend in extends:
    i = i + 1
    # print(extend.text)
print(len(extends))

for element in root.iter():
    i = i + 1
    # print("%s - %s" % (element.tag, element.text))

for element in root.iter("synonym"):
    print("%s - %s" % (element.tag, element.text))
