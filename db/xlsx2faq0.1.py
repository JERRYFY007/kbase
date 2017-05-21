# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xlsx2xml.py
# @time:2017/3/11 0011 20:21

import xlrd

excel_filename = '知识库.xlsx'

workbook = xlrd.open_workbook(excel_filename)
booksheet = workbook.sheet_by_name('Sheet0')

faq_data = []
qa_id = 0
for row in range(booksheet.nrows):
    row_data = []
    for col in range(booksheet.ncols):
        cel = booksheet.cell(row, col)
        val = cel.value
        try:
            val = cel.value
        except:
            pass
        row_data.append(val)
    print(row_data, row_data[0], row_data[1], row_data[2])
    if row_data[0] != "":
        qa_id = qa_id + 1
        faq_data.append("【问题】" + row_data[0] + "\n")
        faq_data.append(row_data[2] + "\n")
        faq_data.append("\n")

open('FAQ_KF.txt', 'w', encoding='utf8').writelines(faq_data)
print("FAQ_KF.txt 文件建立完成! Process FAQs: ", qa_id)

