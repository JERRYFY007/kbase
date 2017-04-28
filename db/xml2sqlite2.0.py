# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xml2sqlite.py
# @time:2017/3/24 0011 20:21

import hashlib
import os
import sqlite3

from lxml import etree

xml_filename1 = 'knowledge.xml'
xml_filename2 = 'keyword.xml'
xml_filename3 = 'keywordfunction.xml'
db_filename = 'knowledge.db'

sql1 = 'create table knowledge_from_xml (id integer primary key autoincrement, qa_id integer, qa_md5 text, question text, answer text)'
sql2 = 'create table extend_from_xml (id integer primary key autoincrement, \
        qa_id integer, ex_id integer, item text, sy_id integer, synonym text)'
sql3 = 'create table keyword_from_xml (id integer primary key autoincrement, \
        qa_id integer, ex_id integer, keyword text, importance text, sy_id integer, synonym text)'
sql4 = 'create table keywordfunction_from_xml (id integer primary key autoincrement, \
        keyword text, importance text, type text, type2 text, sy_id integer, synonym text)'

db_is_new = not os.path.exists(db_filename)
conn = sqlite3.connect(db_filename)
print("Opened database successfully")
if db_is_new:
    print('Need to create schema')
else:
    print('Database exists, assume schema does, too.')
    conn.execute('drop table if exists knowledge_from_xml;')
    conn.execute('drop table if exists extend_from_xml;')
    conn.execute('drop table if exists keyword_from_xml;')
    conn.execute('drop table if exists keywordfunction_from_xml;')
conn.execute(sql1)
conn.execute(sql2)
conn.execute(sql3)
conn.execute(sql4)

# Process knowledge.xml
tree = etree.parse(xml_filename1)
root = tree.getroot()
qa_id = 0
i, j = 0, 0
for knowledge in root:
    qa_id = qa_id + 1
    row_data = []
    ex_id = 0
    for field in knowledge:
        if field.text is None:
            # Process Extend item
            ex_id = ex_id + 1
            for item in field:
                ex_data = []
                sy_id = 0
                for keyword in item:
                    if not keyword.text is None:
                        ex_data.append(keyword.text.strip())
                if len(ex_data) == 1:
                    # print(ex_data)
                    conn.execute("INSERT INTO extend_from_xml(qa_id, ex_id, sy_id,item) VALUES (?,?,?,?)",
                                 (qa_id, ex_id, sy_id, ex_data[0]))
                while len(ex_data) >= 2:
                    sy_id = sy_id + 1
                    conn.execute(
                        "INSERT INTO extend_from_xml(qa_id, ex_id, sy_id,item, synonym) VALUES (?,?,?,?,?)",
                        (qa_id, ex_id, sy_id, ex_data[0], ex_data[1],))
                    # print("Synonym No.: ", sy_id)
                    ex_data.pop(1)
                j = j + sy_id
                # print("Extend No.: ", ex_id)
        else:
            row_data.append(field.text.strip())
    i = i + ex_id
    while len(row_data) > 2:
        conn.execute("INSERT INTO knowledge_from_xml(qa_id, qa_md5, question, answer) VALUES (?,?,?,?)", \
                 (qa_id, hashlib.md5(row_data[0].encode('utf-8')).hexdigest(), row_data[0], row_data[1]))
        row_data.pop(1)
print('Process extend: ' + str(i))
print('Process synonym: ' + str(j))
print("Process QA: ", qa_id)

# Process keyword.xml
root = etree.parse(xml_filename2).getroot()
i, j = 0, 0
omit = False
for element in root:
    category = element.tag
    row_data = []
    sy_id = 0
    for attribute in element:
        row_data.append(attribute.text.strip())
    if len(row_data) == 2:
        conn.execute("INSERT INTO keyword_from_xml(keyword, importance) VALUES (?,?)", row_data)
        i = i + 1
    while len(row_data) >= 3:
        sy_id = sy_id + 1
        conn.execute("INSERT INTO keyword_from_xml(keyword, importance, sy_id, synonym) VALUES (?,?,?,?)",
                     (row_data[0], row_data[1], sy_id, row_data[-1],))
        j = j + 1
        # print(row_data)
        row_data.pop(-1)
print('Process keyword: ' + str(i))
print('Process synonym: ' + str(j))

# Process keywordfunction.xml
root = etree.parse(xml_filename3).getroot()
i, j = 0, 0
for element in root:
    row_data = []
    sy_id = 0
    for attribute in element:
        if not attribute.text is None:
            row_data.append(attribute.text.strip())
    if len(row_data) == 4:
        conn.execute("INSERT INTO keywordfunction_from_xml(keyword,importance,type,type2) VALUES (?,?,?,?)", row_data)
        i = i + 1
    while len(row_data) >= 5:
        sy_id = sy_id + 1
        conn.execute(
            "INSERT INTO keywordfunction_from_xml(keyword,importance,type,type2,sy_id,synonym) VALUES (?,?,?,?,?,?)",
            (row_data[0], row_data[1], row_data[2], row_data[3], sy_id, row_data[-1],))
        j = j + 1
        # print(row_data)
        row_data.pop(-1)
print('Process keyword: ' + str(i))
print('Process synonym: ' + str(j))

conn.commit()
conn.close()
