# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:peewee2.py
# @time:2017/4/1 0001 17:25

import datetime

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)


class Tweet(BaseModel):
    user = ForeignKeyField(User, related_name='tweets')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)


# Connect to the database and create tables:


db.connect()
db.create_tables([User, Tweet])

# Create a few rows:


charlie = User.create(username='charlie')
huey = User(username='huey')
huey.save()

# No need to set `is_published` or `created_date` since they
# will just use the default values we specified.
Tweet.create(user=charlie, message='My first tweet')

# Queries are expressive and composable:


# A simple query selecting a user.
User.get(User.username == 'charles')

# Get tweets created by one of several users. The "<<" operator
# corresponds to the SQL "IN" operator.
usernames = ['charlie', 'huey', 'mickey']
users = User.select().where(User.username << usernames)
tweets = Tweet.select().where(Tweet.user << users)

# We could accomplish the same using a JOIN:
tweets = (Tweet
          .select()
          .join(User)
          .where(User.username << usernames))

# How many tweets were published today?
tweets_today = (Tweet
                .select()
                .where(
    (Tweet.created_date >= datetime.date.today()) &
    (Tweet.is_published == True))
                .count())

# Paginate the user table and show me page 3 (users 41-60).
User.select().order_by(User.username).paginate(3, 20)

# Order users by the number of tweets they've created:
tweet_ct = fn.Count(Tweet.id)
users = (User
         .select(User, tweet_ct.alias('ct'))
         .join(Tweet, JOIN.LEFT_OUTER)
         .group_by(User)
         .order_by(tweet_ct.desc()))

# Do an atomic update
Counter.update(count=Counter.count + 1).where(Counter.url == request.url)
