# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xmlp.py
# @time:2017/3/23 0023 21:35

xml_filename1 = 'knowledge.xml'

import xml.etree.ElementTree as ET

tree = ET.ElementTree(file='knowledge.xml')
root = tree.getroot()
#for child_of_root in root:
    #print(child_of_root.tag, child_of_root.attrib, child_of_root.text)

for elem in tree.iter():
    print(elem.tag, elem.attrib, elem.text)

#for elem in tree.iter(tag='keyword'):
    #print(elem.tag, elem.attrib, elem.text)

#for elem in tree.iterfind('keyword'):
    #print(elem.tag, elem.attrib, elem.text)
