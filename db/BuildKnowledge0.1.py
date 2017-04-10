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
ex_data = []
qa_id = 0
i, j = 0, 0
for knowledge in root:
    qa_id = qa_id + 1
    qa_data = []
    row_data = []
    ex_id = 0
    for field in knowledge:
        if field.text is None:
            ex_id = ex_id + 1
            for item in field:
                for keyword in item:
                    if not keyword.text is None:
                        row_data.append(keyword.text.strip())
                if len(row_data) == 2:
                    ex_data.append(row_data[0] + ',' + str(qa_id) + '-' + str(ex_id) + '\n')
                row_data = []
        else:
            qa_data.append(field.text.strip())
    que_data.append(qa_data[0] + '\n')
    ans_data.append(qa_data[1] + '\n')
print("Process QA: ", qa_id)
open('question.txt', 'w', encoding='utf8').writelines(que_data)
open('answer.txt', 'w', encoding='utf8').writelines(ans_data)
open('extend.dict', 'w', encoding='utf8').writelines(ex_data)
print("Knowledge.xml 文件建立完成! (question.txt & answer.txt & extend.dict)")
