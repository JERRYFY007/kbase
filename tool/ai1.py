# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:ai1.py
# @time:2017/7/1 0001 17:47
from marshmallow import Schema, fields, pprint


class Property(object):
    def __init__(self):
        self.name = ""
        self.ask = ""
        self.resultID = ""
        self.property = []
        self.param = []
        self.similarity = []
        self.synonym_part = []
        self.isDefault = False


class RealProperty(Property):
    pass


class Param:
    def __init__(self):
        self.name = ""
        self.nameEntity = []
        self.length_max = 99
        self.length_min = 1
        self.type = ""
        self.value_default = ""

    pass


class RealParam(Param):
    def __init__(self):
        Param.__init__(self)


class Responce(Schema):
    speak = fields.String()
    show = fields.String()
    eventid = fields.String()
    var = []


class Conversation(Schema):
    id = fields.String()
    input = fields.String()
    responce = fields.Nested(Responce)
    # self.askingParam = RealParam()
    # self.realProperty = RealProperty()


responce = Responce()
responce.speak = "广州:7月3号 周一,26-31° 26° 大雨转雷阵雨 无持续风微风;7月4号 周二,27-33° 雷阵雨 无持续风微风;7月5号 周三,27-34° 雷阵雨 无持续风微风;7月6号 周四,26-34° 雷阵雨 无持续风微风;"
responce.show = responce.speak
conversation = Conversation()
conversation.id = str(1)
conversation.input = "广州今天的天气怎样？"
# print(conversation.input)

result, errors = Responce().dump(responce)
pprint(result)

result, errors = Conversation().dump(conversation)
pprint(result)
