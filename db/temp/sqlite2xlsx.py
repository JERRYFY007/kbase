# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:xlsx2xml.py
# @time:2017/3/11 0011 20:21
import sqlite3

from xlsxwriter.workbook import Workbook

excel_filename = 'kbase.xlsx'
db_filename = 'kbase.db'
sql1 = "select * from kbase"
sql2 = "select question,question1,question2,answer from kbase"

workbook = Workbook(excel_filename)
worksheet = workbook.add_worksheet()

conn = sqlite3.connect(db_filename)
c = conn.cursor()
c.execute(sql1)
mysel = c.execute(sql2)
for i, row in enumerate(mysel):
    for j, value in enumerate(row):
        worksheet.write(i, j, row[j])
workbook.close()
conn.close()
