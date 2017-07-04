# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:ai4.py
# @time:2017/7/3 0003 11:08
import json

import requests

# Make the same request we did earlier, but with the coordinates of San Francisco instead.
parameters = {"input": '{"input":"广州今天的天气怎样？"}'}
response = requests.get("http://39.108.135.114:8001/simpleMobile/getConversation.sc?", params=parameters)

print(response)
# Headers is a dictionary
print(response.headers)
# Get the content-type from the dictionary.
print(response.headers["content-type"])
# print(response.content.decode("utf-8"))

data = response.json()
print(type(data))
print(data)
print(json.dumps(data, ensure_ascii=False, indent=2))

# 将一个Python数据结构转换为JSON
# json_str = json.dumps(data)
# data = json.loads(json_str)
# print(json.dumps(json_str, ensure_ascii=False, indent=2))
