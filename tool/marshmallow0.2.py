# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:marshmallow0.2.py
# @time:2017/7/1 0001 11:36
import datetime as dt

from marshmallow import Schema


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


from pprint import pprint

user_data = {
    'created_at': '2014-08-11T05:26:03.869245',
    'email': u'ken@yahoo.com',
    'name': u'Ken'
}
schema = UserSchema()
result = schema.load(user_data)
pprint(result.data)
# {'name': 'Ken',
#  'email': 'ken@yahoo.com',
#  'created_at': datetime.datetime(2014, 8, 11, 5, 26, 3, 869245)},

from marshmallow import Schema, fields, post_load


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data):
        return User(**data)


user_data = {
    'name': 'Ronnie',
    'email': 'ronnie@stones.com'
}
schema = UserSchema()
result = schema.load(user_data)
pprint(result.data)  # => <User(name='Ronnie')>

user1 = User(name="Mick", email="mick@stones.com")
user2 = User(name="Keith", email="keith@stones.com")
users = [user1, user2]
schema = UserSchema(many=True)
result = schema.dump(users)  # OR UserSchema().dump(users, many=True)
pprint(result.data)
# [{'name': u'Mick',
#   'email': u'mick@stones.com',
#   'created_at': '2014-08-17T14:58:57.600623+00:00'}
#  {'name': u'Keith',
#   'email': u'keith@stones.com',
#   'created_at': '2014-08-17T14:58:57.600623+00:00'}]

data, errors = UserSchema().load({'email': 'foo'})
errors  # => {'email': ['"foo" is not a valid email address.']}
# OR, equivalently
result = UserSchema().load({'email': 'foo'})
result.errors  # => {'email': ['"foo" is not a valid email address.']}
