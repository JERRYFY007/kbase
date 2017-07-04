# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:marshmallow0.1.py
# @time:2017/7/1 0001 11:34

import datetime as dt


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


from marshmallow import pprint

user = User(name="Monty", email="monty@python.org")
schema = UserSchema()
result = schema.dump(user)
pprint(result.data)
# {"name": "Monty",
#  "email": "monty@python.org",
#  "created_at": "2014-08-17T14:54:16.049594+00:00"}

json_result = schema.dumps(user)
pprint(json_result.data)
# '{"name": "Monty", "email": "monty@python.org", "created_at": "2014-08-17T14:54:16.049594+00:00"}'

summary_schema = UserSchema(only=('name', 'email'))
summary_schema.dump(user).data
# {"name": "Monty Python", "email": "monty@python.org"}
