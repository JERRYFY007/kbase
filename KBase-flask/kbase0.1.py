# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:kbase0.1.py
# @time:2017/3/14 0014 15:36
from __future__ import unicode_literals

import sqlite3

import click
from flask import Flask, render_template, g, current_app, request
from flask_paginate import Pagination, get_page_args

click.disable_unicode_literals_warning = True

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db_filename = 'kbase.db'


@app.before_request
def before_request():
    g.conn = sqlite3.connect(db_filename)
    g.conn.row_factory = sqlite3.Row
    g.cur = g.conn.cursor()


@app.teardown_request
def teardown(error):
    if hasattr(g, 'conn'):
        g.conn.close()


@app.route('/')
def index():
    g.cur.execute('select count(*) from kbase where question not like ""')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args()
    sql = 'select question,answer from kbase where question not like "" order by id limit {}, {}' \
        .format(offset, per_page)
    g.cur.execute(sql)
    users = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='users',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('index.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@app.route('/users/', defaults={'page': 1})
@app.route('/users', defaults={'page': 1})
@app.route('/users/page/<int:page>/')
@app.route('/users/page/<int:page>')
def users(page):
    g.cur.execute('select count(*) from kbase where question not like ""')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args()
    sql = 'select question,answer from kbase where question not like "" order by id limit {}, {}' \
        .format(offset, per_page)
    g.cur.execute(sql)
    users = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='users',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('index.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           active_url='users-page-url',
                           )


@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sql = 'select count(*) from kbase where question like ?'
        args = ('%{}%'.format(request.form['search']),)
        g.cur.execute(sql, args)
        total = g.cur.fetchone()[0]

        page, per_page, offset = get_page_args()
        sql = 'select * from kbase where question like ? limit {}, {}'
        g.cur.execute(sql.format(offset, per_page), args)
        users = g.cur.fetchall()
        pagination = get_pagination(page=page,
                                    per_page=per_page,
                                    total=total,
                                    record_name='users',
                                    )
        return render_template('index.html', users=users,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               )
    # return redirect(url_for('search'))
    return render_template('search.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        g.cur.execute('insert into kbase (question, question1, question2, answer) values (?, ?, ?, ?)',
                      [request.form['question'], request.form['question1'], request.form['question2'],
                       request.form['answer']])
        g.conn.commit()
        sql = 'select count(*) from kbase where question like ?'
        args = ('%{}%'.format(request.form['question']),)
        g.cur.execute(sql, args)
        total = g.cur.fetchone()[0]

        page, per_page, offset = get_page_args()
        sql = 'select * from kbase where question like ? limit {}, {}'
        g.cur.execute(sql.format(offset, per_page), args)
        users = g.cur.fetchall()
        pagination = get_pagination(page=page,
                                    per_page=per_page,
                                    total=total,
                                    record_name='users',
                                    )
        return render_template('index.html', users=users,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               )
    # return redirect(url_for('add'))
    return render_template('add.html')


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')


def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )


@click.command()
@click.option('--port', '-p', default=5000, help='listening port')
def run(port):
    app.run(debug=True, port=port)


if __name__ == '__main__':
    run()
