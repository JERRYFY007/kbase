# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xml2sqlite.py
# @time:2017/3/24 0011 20:21

import hashlib
import os
import sqlite3

from lxml import etree


def node_text(node):
    result = ""
    for text in node.itertext():
        result = result + text
    return result


xml_filename1 = 'knowledge.xml'
xml_filename2 = 'keyword.xml'
xml_filename3 = 'keywordfunction.xml'
db_filename = 'knowledge.db'

sql1 = 'create table knowledge_from_xml (id integer primary key autoincrement, qa_md5 text, question text, answer text)'
sql2 = 'create table extend_from_xml (id integer primary key autoincrement, \
        qa_id integer,ex_id integer,sy_id integer,item text, omit text, synonym text)'
sql3 = 'create table keyword_from_xml (id integer primary key autoincrement, \
        qa_id integer, ex_id integer, keyword text, importance text, synonym text)'
sql4 = 'create table keywordfunction_from_xml (id integer primary key autoincrement, \
        keyword text, importance text, type text, type2 text, synonym text)'

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

parser = etree.XMLParser()

# Process knowledge.xml
tree = etree.parse(xml_filename1, parser)
root = tree.getroot()
qa_id = 0
for knowledge in root:
    qa_id = qa_id + 1
    row_data = []
    ex_id = 0
    for field in knowledge:
        if not field.text is None:
            row_data.append(field.text.strip())
        else:
            # Process Extend item
            ex_id = ex_id + 1
            for item in field:
                ex_data = []
                sy_id = 0
                for keyword in item:
                    if not keyword.text is None:
                        ex_data.append(keyword.text.strip())
                if len(ex_data) == 2:
                    # print(ex_data)
                    conn.execute("INSERT INTO extend_from_xml(qa_id, ex_id, sy_id,item, omit) VALUES (?,?,?,?,?)",
                                 (qa_id, ex_id, sy_id, ex_data[0], ex_data[1],))
                while len(ex_data) >= 3:
                    sy_id = sy_id + 1
                    conn.execute(
                        "INSERT INTO extend_from_xml(qa_id, ex_id, sy_id,item, omit,synonym) VALUES (?,?,?,?,?,?)",
                        (qa_id, ex_id, sy_id, ex_data[0], ex_data[1], ex_data[-1],))
                    # print("Synonym No.: ", sy_id)
                    ex_data.pop(-1)
                    # print("Extend No.: ", ex_id)
    if len(row_data) == 2:
        conn.execute("INSERT INTO knowledge_from_xml(qa_md5, question, answer) VALUES (?,?,?)", \
                     (hashlib.md5(row_data[0].encode('utf-8')).hexdigest(), row_data[0], row_data[1]))
print("QA No.: ", qa_id)

# Process keyword.xml
root = etree.parse(xml_filename2).getroot()
i, j = 0, 0
omit = False
for element in root:
    category = element.tag
    row_data = []
    for attribute in element:
        row_data.append(attribute.text.strip())
    if len(row_data) == 2:
        conn.execute("INSERT INTO keyword_from_xml(keyword,importance) VALUES (?,?)", row_data)
        i = i + 1
    while len(row_data) >= 3:
        conn.execute("INSERT INTO keyword_from_xml(keyword,importance,synonym) VALUES (?,?,?)",
                     (row_data[0], row_data[1], row_data[-1],))
        j = j + 1
        # print(row_data)
        row_data.pop(-1)
print('Process keyword: ' + str(i))
print('Process synonym: ' + str(j))

# Process keywordfunction.xml
root = etree.parse(xml_filename3).getroot()
i, j = 0, 0
for element in root:
    category = element.tag
    row_data = []
    for attribute in element:
        if not attribute.text is None:
            row_data.append(attribute.text.strip())
    if len(row_data) == 4:
        conn.execute("INSERT INTO keywordfunction_from_xml(keyword,importance,type,type2) VALUES (?,?,?,?)", row_data)
        i = i + 1
    while len(row_data) >= 5:
        conn.execute("INSERT INTO keywordfunction_from_xml(keyword,importance,type,type2,synonym) VALUES (?,?,?,?,?)",
                     (row_data[0], row_data[1], row_data[2], row_data[3], row_data[-1],))
        j = j + 1
        # print(row_data)
        row_data.pop(-1)
print('Process keyword: ' + str(i))
print('Process synonym: ' + str(j))

conn.commit()
conn.close()
