# -*- coding: utf-8 -*-
from lxml import etree

xml_filename1 = 'knowledge.xml'

# Process knowledge.xml
tree = etree.parse(xml_filename1)
root = tree.getroot()

que_data = []
ans_data = []
ex_data, ex2_data = [], []
qa_id = 0
ex_nu = 0
for knowledge in root:
    qa_id = qa_id + 1
    qa_data = []
    ex_id = 0
    for field in knowledge:
        if field.text is None:
            ex_id = ex_id + 1
            for item in field:
                row_data = []
                ky_id = 0
                for keyword in item:
                    ky_id += 1
                    row_data.append(keyword.text.strip())
                if len(row_data) == 2:
                    ex_data.append(row_data[0].lower() + ',' + str(qa_id) + '-' + str(ex_id) + '-' + str(ky_id) + '\n')
                    ex2_data.append(row_data[0].lower() + '/')
                elif len(row_data) >= 3:
                    ex2_data.append(row_data[-1].lower() + '|')
                    row_data.pop(-1)
            ex2_data.append(',' + str(qa_id) + '-' + str(ex_id) + '\n')
        else:
            qa_data.append(field.text.strip())
    ex_nu += ex_id
    que_data.append(qa_data[0] + '\n')
    ans_data.append(qa_data[1] + '\n')
print("Process QA: ", qa_id)
print("Process Extend: ", ex_nu)
open('question.txt', 'w', encoding='utf8').writelines(que_data)
open('answer.txt', 'w', encoding='utf8').writelines(ans_data)
open('extend1.dict', 'w', encoding='utf8').writelines(ex_data)
open('extend2.dict', 'w', encoding='utf8').writelines(ex2_data)
print("Knowledge.xml 文件建立完成! (question.txt & answer.txt & extend.dict)")
