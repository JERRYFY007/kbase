# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:peewee1.py
# @time:2017/4/1 0001 11:28
from peewee import *

db = SqliteDatabase('../knowledge.db')


class keyword_from_xlsx(Model):
    kw_md5 = CharField()
    keyword = CharField()
    sy_id = IntegerField()
    synonym = CharField()

    class Meta:
        database = db  # This model uses the "people.db" database.


# query = (keyword.select().where((keyword.keyword = '') & (keyword.synonym = '')))
for keyword1 in keyword_from_xlsx.select():
    # print(keyword1.keyword, keyword1.sy_id, keyword1.synonym)
    for keyword2 in keyword_from_xlsx.select():
        if keyword2.keyword == keyword1.keyword:
            print('Found:', keyword1.keyword, keyword1.synonym, keyword2.synonym)

db.close()
