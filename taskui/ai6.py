# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:ai4.py
# @time:2017/7/3 0003 11:08
import requests

# Make the same request we did earlier, but with the coordinates of San Francisco instead.
parameters = {"input": '{in:广州今天的天气怎样？}'}
parameters = {"input": '{in:天气如何？}'}
parameters = {"input": '{in:上个月电费？}'}
response = requests.get("http://39.108.135.114:8001/simpleMobile/getConversation.sc?", params=parameters)

print(response)
# Headers is a dictionary
print(response.headers)
# Get the content-type from the dictionary.
print(response.headers["content-type"])
# print(response.content.decode("utf-8"))

data = response.json()
print(type(data))
# print(data)
# print(json.dumps(data, ensure_ascii=False, indent=2))
print('input:', data['input'])
print(type(data['input']))
print("-" * 60)
print(data["realProperty"])
print("-" * 60)
print("askingParam:", data["askingParam"])
print("-" * 60)
print(data["realProperty"]["realproperty"]["realparam"])
print("-" * 60)
print(data["realProperty"]["realproperty"]["realparam"][0])
print(data["realProperty"]["realproperty"]["realparam"][1])
print("-" * 60)
print(data["realProperty"]["realproperty"]["realparam"][0]["nameEntity"])
print(data["realProperty"]["realproperty"]["realparam"][1]["nameEntity"])
print("-" * 60)
print(data["realProperty"]["realproperty"]["realparam"][0]["nameEntity"]["including"])
print("-" * 60)
print("Respose Show: ", data['responce']['show'])
# print(data['responce']['speak'])
# print(json.dumps(data['responce'], ensure_ascii=False, indent=2))
for (k, v) in data.items():
    print("dict[%s]=" % k, v)
