# -*- coding: utf-8 -*-
from lxml import etree

xml_filename1 = 'knowledge.xml'

# Process knowledge.xml
tree = etree.parse(xml_filename1)
root = tree.getroot()

que_data = []
ans_data = []
ex_data = ['Item, qa_id:ex_id, kw_id, sy_id']
qa_id = 0
ex_no, kw_no, sy_no = 0, 0, 0
dict_ex = {}
dict_extend, dict_extend_item, dict_extend_point = {}, {}, {}
for knowledge in root:
    qa_id = qa_id + 1
    qa_data = []
    ex_id = 0
    for field in knowledge:
        if field.text is None:
            ex_id = ex_id + 1
            kw_id = 0
            extend_item = []
            qa_ex = str(qa_id) + ',' + str(ex_id)
            dict_extend_point[qa_ex] = 0.0
            for item in field:
                row_data = []
                kw_id += 1
                for keyword in item:
                    sy_id = 0
                    row_data.append(keyword.text.strip())
                    extend_item.append(keyword.text.strip())
                sy_no += len(row_data) - 2
                while len(row_data) >= 3:
                    sy_id = len(row_data) - 2
                    ex_data.append('\n' + row_data[-1].lower() + ',' + str(qa_id) + ':' + str(ex_id) + ',' + str(kw_id) + ',' + str(sy_id))
                    extend = row_data[-1].lower()
                    if extend in dict_ex:
                        temp = dict_ex.get(extend)
                        temp.append(qa_ex)
                        dict_ex[extend] = temp
                    else:
                        temp = []
                        temp.append(qa_ex)
                        dict_ex[extend] = temp
                    row_data.pop(-1)
                if len(row_data) == 2:
                    sy_id = 0
                    ex_data.append('\n' + row_data[0].lower() + ',' + str(qa_id) + ':' + str(ex_id) + ',' + str(kw_id) + ',' + str(sy_id))
                    extend = row_data[0].lower()
                    if extend in dict_ex:
                        temp = dict_ex.get(extend)
                        temp.append(qa_ex)
                        dict_ex[extend] = temp
                    else:
                        temp = []
                        temp.append(qa_ex)
                        dict_ex[extend] = temp
            if extend_item:
                dict_extend_item[qa_ex] = extend_item
            kw_no += kw_id
        else:
            qa_data.append(field.text.strip())
    ex_no += ex_id
    que_data.append(qa_data[0] + '\n')
    ans_data.append(qa_data[1] + '\n')
#for k, v in dict_extend_item.items():
#   print(k, v)
# print(len(dict_ex.get('深圳城中村集合')))
print("Process Extend Dict: ", len(dict_ex))
print("Process Extend Dict: ", len(dict_extend))
print("Process Extend Item Dict: ", len(dict_extend_item))
print("Process Extend Point Dict: ", len(dict_extend_point))
print("Process QA: ", qa_id)
print("Process Extend: ", ex_no)
print("Process Keyword: ", kw_no)
print("Process Local Synonym: ", sy_no)
open('question.txt', 'w', encoding='utf8').writelines(que_data)
open('answer.txt', 'w', encoding='utf8').writelines(ans_data)
open('extend.dict', 'w', encoding='utf8').writelines(ex_data)
print("Knowledge.xml 文件建立完成! (question.txt & answer.txt & extend.dict)")
