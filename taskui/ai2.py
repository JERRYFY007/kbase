# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:ai1.py
# @time:2017/7/3 0003 10:50
import datetime as dt


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
        self.friends = []
        self.employer = None


class Blog(object):
    def __init__(self, title, author):
        self.title = title
        self.author = author  # A User object


from marshmallow import Schema, fields, pprint


class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()


class BlogSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema)


user = User(name="Monty", email="monty@python.org")
blog = Blog(title="Something Completely Different", author=user)
result, errors = BlogSchema().dump(blog)
pprint(result)
# {'title': u'Something Completely Different',
# {'author': {'name': u'Monty',
#             'email': u'monty@python.org',
#             'created_at': '2014-08-17T14:58:57.600623+00:00'}}
