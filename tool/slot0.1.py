# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:slot0.1.py
# @time:2017/6/21 0021 16:03

input_txt = '查询5月份的电费'

domain = '电费'
intent = '电费查询'

slot = {}
slot['domain'] = domain
slot['intent'] = intent
slot['userid'] = '88888'
slot['date'] = '201705'

print(domain)
print(intent)
print(slot)
