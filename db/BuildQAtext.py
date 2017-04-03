# -*- coding: utf-8 -*-
import string
import re
from lxml import etree

xml_filename1 = 'knowledge.xml'

# Process knowledge.xml
tree = etree.parse(xml_filename1)
root = tree.getroot()

que_data = []
ans_data = []
qa_id = 0
i, j = 0, 0
for knowledge in root:
    qa_id = qa_id + 1
    row_data = []
    for field in knowledge:
        if field.text is None:
            break
        else:
            row_data.append(field.text.strip())
    print(row_data[0])
    que_data.append(row_data[0] + '\n')
    print(row_data[1])
    ans_data.append(row_data[1] + '\n')
print("Process QA: ", qa_id)
open('question.txt', 'w', encoding='utf8').writelines(que_data)
open('answer.txt', 'w', encoding='utf8').writelines(ans_data)
print("最终QA文件建立完成! (question.txt & answer.txt)")
