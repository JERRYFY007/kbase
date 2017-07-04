# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:ai5.py
# @time:2017/7/3 0003 12:47
import python_jsonschema_objects as pjs

schema = {'id': '', 'input': '{"input":"广州今天的天气怎样？"}', 'realProperty': {'realproperty': {'realparam': [
    {'value': '广州', 'name': '请问要查哪个城市的天气', 'nameEntity': {'name': '城市名', 'special': False,
                                                          'including': ['深圳', '广州', '北京', '上海', '南京', '重庆', '苏州', '珠海',
                                                                        '香港']}, 'length_max': 99, 'length_min': 1,
     'type': 'String'},
    {'value': '2017年7月3日 0时0分0秒', 'name': '请问要查哪天的天气', 'nameEntity': {'name': '时间', 'special': True, 'including': []},
     'length_max': 99, 'length_min': 1, 'type': 'String', 'value_default': '今天'}], 'name': '信息', 'ask': '查询气温',
    'resultID': '通用_天气',
    'isDefault': True,
    'property': [], 'param': [
        {'name': '请问要查哪个城市的天气', 'nameEntity': {'name': '城市名', 'special': False,
                                               'including': ['深圳', '广州', '北京', '上海', '南京', '重庆', '苏州', '珠海', '香港']},
         'length_max': 99, 'length_min': 1, 'type': 'String'},
        {'name': '请问要查哪天的天气', 'nameEntity': {'name': '时间', 'special': True, 'including': []}, 'length_max': 99,
         'length_min': 1, 'type': 'String', 'value_default': '今天'}], 'similarity': [], 'synonym_part': []},
    'realparam': [], 'name': '天气',
    'isDefault': False, 'property': [
        {'name': '信息', 'ask': '查询气温', 'resultID': '通用_天气', 'isDefault': True, 'property': [], 'param': [
            {'name': '请问要查哪个城市的天气', 'nameEntity': {'name': '城市名', 'special': False,
                                                   'including': ['深圳', '广州', '北京', '上海', '南京', '重庆', '苏州', '珠海', '香港']},
             'length_max': 99, 'length_min': 1, 'type': 'String'},
            {'name': '请问要查哪天的天气', 'nameEntity': {'name': '时间', 'special': True, 'including': []}, 'length_max': 99,
             'length_min': 1, 'type': 'String', 'value_default': '今天'}], 'similarity': [], 'synonym_part': []}],
    'param': [], 'similarity': [],
    'synonym_part': []}, 'responce': {
    'speak': '广州:7月3号 周一,26-31° 26° 大雨转雷阵雨 无持续风微风;7月4号 周二,27-33° 雷阵雨 无持续风微风;7月5号 周三,27-34° 雷阵雨 无持续风微风;7月6号 周四,26-34° 雷阵雨 无持续风微风;',
    'show': '广州:7月3号 周一,26-31° 26° 大雨转雷阵雨 无持续风微风;7月4号 周二,27-33° 雷阵雨 无持续风微风;7月5号 周三,27-34° 雷阵雨 无持续风微风;7月6号 周四,26-34° 雷阵雨 无持续风微风;',
    'eventid': '', 'var': []}}
schema = {
    "title": "Example Schema",
    "type": "object",
    "properties": {
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "age": {
            "description": "Age in years",
            "type": "integer",
            "minimum": 0
        },
        "dogs": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 4
        },
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "state": {"type": "string"}
            },
            "required": ["street", "city"]
        },
        "gender": {
            "type": "string",
            "enum": ["male", "female"]
        },
        "deceased": {
            "enum": ["yes", "no", 1, 0, "true", "false"]
        }
    },
    "required": ["firstName", "lastName"]
}

builder = pjs.ObjectBuilder(schema)
ns = builder.build_classes()
Person = ns.ExampleSchema
james = Person(firstName="James", lastName="Bond")
print(james.lastName)
print(james)
james.age = 42
print(james.serialize())
