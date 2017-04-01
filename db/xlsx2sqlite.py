# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xlsx2xml.py
# @time:2017/3/11 0011 20:21

import hashlib
import os
import sqlite3

import xlrd

excel_filename = '知识库.xlsx'
db_filename = 'knowledge.db'
sql1 = 'create table knowledge_from_xlsx (id integer primary key autoincrement, qa_id integer, qa_md5 text, question text, answer text)'
sql2 = 'create table extend_from_xlsx (id integer primary key autoincrement, qa_id integer, ex_id integer, item text)'
sql3 = 'create table keyword_from_xlsx (id integer primary key autoincrement, qa_id integer, ex_id integer, keyword text, sy_id integer, synonym text)'

workbook = xlrd.open_workbook(excel_filename)
booksheet = workbook.sheet_by_name('Sheet0')
db_is_new = not os.path.exists(db_filename)
conn = sqlite3.connect(db_filename)
print("Opened database successfully")
if db_is_new:
    print ('Need to create schema')
else:
    print ('Database exists, assume schema does, too.')
    conn.execute('drop table if exists knowledge_from_xlsx;')
    conn.execute('drop table if exists extend_from_xlsx;')
    conn.execute('drop table if exists keyword_from_xlsx;')
conn.execute(sql1)
conn.execute(sql2)
conn.execute(sql3)

i, j, qa_id = 0, 0, 0
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
    #print(row_data, row_data[0], row_data[1], row_data[2], row_data[3])
    if row_data[0] == "标准问题":
        continue
    i = i + 1
    ex_id = 0
    if row_data[0] != "":
        qa_id = qa_id + 1
        conn.execute("INSERT INTO knowledge_from_xlsx(qa_id, qa_md5, question, answer) VALUES (?,?,?,?)", \
                     (qa_id, hashlib.md5(row_data[0].encode('utf-8')).hexdigest(), row_data[0], row_data[2]))
    else:
        ex_id = ex_id + 1
        conn.execute("INSERT INTO extend_from_xlsx(qa_id, ex_id, item) VALUES (?,?,?)", (qa_id, ex_id, row_data[1]))
    j = j + ex_id
print('Process QA: ', qa_id)
print('Process extend: ' + str(j))

conn.commit()
conn.close()
