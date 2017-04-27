# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xlsx2xml.py
# @time:2017/4/27 0011 16:21
# knowledge.xml格式修改，增加分支问题branch
from lxml import etree

xml_filename1 = 'knowledge.xml'

# Process knowledge.xml
tree = etree.parse(xml_filename1)
root = tree.getroot()

que_data, ans_data, branch = [], [], []
extend_item = ['qa_ex_id,Item,canOmit,synonym']
extend_point = ['qa_ex_id,max,match,unmatch,best']
dict_extend = ['qa_ex_id,Item']
dict_extend_synonym = ['qa_ex_id,Item']
qa_id = 0
ex_no, kw_no, sy_no = 0, 0, 0

for knowledge in root:
    qa_id = qa_id + 1
    qa_data = []
    ex_id = 0
    for field in knowledge:
        if field.text is None:  # 处理extend
            ex_id = ex_id + 1
            br_id, kw_id = 0, 0
            extend = []
            extend_synonym = []
            qa_ex = str(qa_id) + ':' + str(ex_id)  # 生成标准问题加扩展问的id
            extend_point.append('\n' + qa_ex + ',' + '0.0' + ',' + '0.0' + ',' + '0.0' + ',' + '0.0')  # 初始化各类评分为零
            for item in field:	
                row_data = []  # 初始化临时列表
                kw_id += 1
                for keyword in item:
                    row_data.append(keyword.text.strip())  # 循环读取extend数据至临时列表
                sy_no += len(row_data) - 2  # 统计局部同义词数量
                if len(row_data) == 2:  # 无局部同义词的处理
                    extend_item.append('\n' + qa_ex + ',' + row_data[0].lower() + ',' + row_data[1].lower())
                    extend.append(row_data[0].lower() + ';')
                    extend_synonym.append(row_data[0].lower() + ';')
                else:  # 有局部同义词的处理
                    extend_synonym.append(row_data[0].lower()) # 局部同义词列表
                    while len(row_data) >= 3:  # 多个局部同义词循环处理
                        extend_item.append('\n' + qa_ex + ',' + row_data[0].lower() + ',' + row_data[1].lower() + ',')
                        extend_item.append(row_data[-1].lower())
                        extend.append(row_data[-1].lower() + ';')
                        extend_synonym.append('|' + row_data[-1].lower())
                        row_data.pop(-1)  # 去掉局部同义词列表最后一个
                    extend_synonym.append(';')
            if extend:  # 处理扩展问题
                dict_extend.append('\n' + qa_ex + ',')
                dict_extend.extend(extend)
                dict_extend_synonym.append('\n' + qa_ex + ',')
                dict_extend_synonym.extend(extend_synonym)
            kw_no += kw_id
        else:  # 处理标准问题及标准答案
            if field.tag == "question":
                que_data.append(str(qa_id) + ',' + field.text.strip() + '\n')
            if field.tag == "answer":
                ans_data.append(str(qa_id) + ',' + field.text.strip() + '\n')
            if field.tag == "branch":
                br_id += 1
                branch.append(str(qa_id) + ':' + str(br_id) + ',' + field.text.strip() + '\n')
    ex_no += ex_id
print("Process QA: ", qa_id)
print("Process Extend: ", ex_no)
print("Process Keyword: ", kw_no)
print("Process Local Synonym: ", sy_no)
open('qa_question.txt', 'w', encoding='utf8').writelines(que_data)
open('qa_answer.txt', 'w', encoding='utf8').writelines(ans_data)
open('qa_branch.txt', 'w', encoding='utf8').writelines(branch)
open('extend_item.df', 'w', encoding='utf8').writelines(extend_item)
open('extend_point.df', 'w', encoding='utf8').writelines(extend_point)
open('extend_item.dict', 'w', encoding='utf8').writelines(dict_extend)
open('extend_item_sy.dict', 'w', encoding='utf8').writelines(dict_extend_synonym)
print("Knowledge.xml 文件建立完成! (question & answer & branch & extend_item.df & extend_point.df)")
