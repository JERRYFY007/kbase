# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xlsx2xml.py
# @time:2017/3/11 0011 20:21

import hashlib
import os
import re
import sqlite3

import xlrd

excel_filename = '知识库.xlsx'
db_filename = 'knowledge.db'
sql1 = 'create table knowledge_from_xlsx (id integer primary key autoincrement, qa_id integer, qa_md5 text, question text, answer text)'
sql2 = 'create table extend_from_xlsx (id integer primary key autoincrement, qa_id integer, ex_id integer, item_md5 text, item text, sy_id integer, synonym text)'
sql3 = 'create table keyword_from_xlsx (id integer primary key autoincrement, kw_md5 text, keyword text, sy_id integer, synonym text)'

workbook = xlrd.open_workbook(excel_filename)
booksheet = workbook.sheet_by_name('Sheet0')
db_is_new = not os.path.exists(db_filename)
conn = sqlite3.connect(db_filename)
cur = conn.cursor()
print("Opened database successfully")

if db_is_new:
    print('Need to create schema')
else:
    print('Database exists, assume schema does, too.')
    cur.execute('drop table if exists knowledge_from_xlsx;')
    cur.execute('drop table if exists extend_from_xlsx;')
    conn.execute('drop table if exists keyword_from_xlsx;')
cur.execute(sql1)
cur.execute(sql2)
cur.execute(sql3)

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
    # print(row_data, row_data[0], row_data[1], row_data[2], row_data[3])
    if row_data[0] == "标准问题":
        continue
    i = i + 1
    if row_data[0] != "":
        qa_id = qa_id + 1
        ex_id = 0
        cur.execute("INSERT INTO knowledge_from_xlsx(qa_id, qa_md5, question, answer) VALUES (?,?,?,?)", \
                    (qa_id, hashlib.md5(row_data[0].encode('utf-8')).hexdigest(), row_data[0], row_data[2]))
    else:
        temp_extend = re.sub(r'[[]', '', row_data[1])
        extends = re.split(r'[]]', temp_extend)
        extends.pop(-1)
        ex_id = ex_id + 1
        for extend in extends:
            if re.search(r'[|]', extend) is None:
                cur.execute("INSERT INTO extend_from_xlsx (qa_id, ex_id, item_md5, item) VALUES (?,?,?,?)",
                            (qa_id, ex_id, hashlib.md5(extend.encode('utf-8')).hexdigest(), extend))
                # 查询数据库表 keyword 中有没有相同的关键词，如果没有就加入表中
                args = extend
                cur.execute("SELECT count(*) FROM keyword_from_xlsx WHERE keyword like ?", (args,))
                total = cur.fetchone()[0]
                if total == 0:
                    cur.execute("INSERT INTO keyword_from_xlsx(kw_md5, keyword) VALUES (?,?)",
                                (hashlib.md5(extend.encode('utf-8')).hexdigest(), extend))
                    print("Add one new keyword:", extend)
            else:
                synonyms = re.split(r'[|]', extend)
                sy_id = 0
                # print(synonyms)
                for synonym in synonyms:
                    sy_id = sy_id + 1
                    if len(synonyms) > sy_id:
                        cur.execute(
                            "INSERT INTO extend_from_xlsx(qa_id, ex_id, item_md5, item, sy_id, synonym) VALUES (?,?,?,?,?,?)", \
                            (qa_id, ex_id, hashlib.md5(synonyms[0].encode('utf-8')).hexdigest(), synonyms[0], sy_id,
                             synonyms[sy_id]))
                        # 查询数据库表 keyword 中有没有相同的关键词，如果没有就加入表中
                        args = synonyms[0]
                        cur.execute("SELECT count(*) FROM keyword_from_xlsx WHERE keyword like ?", (args,))
                        total = cur.fetchone()[0]
                        if total == 0:
                            cur.execute(
                                "INSERT INTO keyword_from_xlsx(kw_md5, keyword, sy_id, synonym) VALUES (?,?,?,?)", \
                                (hashlib.md5(synonyms[0].encode('utf-8')).hexdigest(), synonyms[0], sy_id,
                                 synonyms[sy_id]))
                            print("Add one keyword with new synonym:", synonyms[0], sy_id, synonyms[sy_id])
                        else:
                            # 查询数据库表 keyword 中有没有相同的同义词，如果没有就加入表中；如果有再看关键词是否一样
                            args = synonyms[sy_id]
                            cur.execute("SELECT * FROM keyword_from_xlsx WHERE synonym like ?", (args,))
                            keyword = cur.fetchone()
                            if keyword is None:
                                cur.execute(
                                    "INSERT INTO keyword_from_xlsx(kw_md5, keyword, sy_id, synonym) VALUES (?,?,?,?)", \
                                    (hashlib.md5(synonyms[0].encode('utf-8')).hexdigest(), synonyms[0], sy_id,
                                     synonyms[sy_id]))
                                print("Add one keyword with new synonym:", synonyms[0], sy_id, synonyms[sy_id])
                            else:
                                print(args, '---', keyword[2], synonyms[0], '---', keyword[4], synonyms[sy_id])
                                # if keyword[2] != synonyms[0]:
                                # print(keyword[2], synonyms[0], '---', keyword[4], synonyms[sy_id])
                                #   cur.execute("INSERT INTO keyword_from_xlsx(kw_md5, keyword, sy_id, synonym) VALUES (?,?,?,?)",\
                                #          (hashlib.md5(synonyms[0].encode('utf-8')).hexdigest(), synonyms[0], sy_id, synonyms[sy_id]))
                                # print("Add One keyword with synonym:", synonyms[0], sy_id, synonyms[sy_id])
                j = j + sy_id
        i = i + ex_id
print('Process QAes: ', qa_id)
print('Process extends: ', i)
print('Process synonyms: ', j)

cur.close()
conn.commit()
conn.close()
