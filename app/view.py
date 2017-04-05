# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:view.py
# @time:2017/3/29
from __future__ import unicode_literals
from flask import render_template, g, current_app, request
from flask_paginate import Pagination, get_page_args
import sqlite3
import click
from app import app, knowledge, segment


click.disable_unicode_literals_warning = True

app.config.from_pyfile('app.cfg')
db_filename = 'knowledge.db'


@app.before_request
def before_request():
    g.conn = sqlite3.connect(db_filename)
    g.conn.row_factory = sqlite3.Row
    g.cur = g.conn.cursor()


def query_db(query, args=(), one=False):
    cur = g.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_request
def teardown(error):
    if hasattr(g, 'conn'):
        g.conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/knowledges/', defaults={'page': 1})
@app.route('/knowledges', defaults={'page': 1})
@app.route('/knowledges/page/<int:page>/')
@app.route('/knowledges/page/<int:page>')
def knowledges(page):
    g.cur.execute('select count(*) from knowledge_from_xml where question not like ""')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args()
    sql = 'select * from knowledge_from_xml where question not like "" order by id limit {}, {}' \
        .format(offset, per_page)
    g.cur.execute(sql)
    knowledges = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                format_total=True,
                                format_number=True,
                                )
    return render_template('knowledge.html', knowledges=knowledges,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           active_url='knowledges-page-url',
                           )


@app.route('/keywords/', defaults={'page': 1})
@app.route('/keywords', defaults={'page': 1})
@app.route('/keywords/page/<int:page>/')
@app.route('/keywords/page/<int:page>')
def keywords(page):
    g.cur.execute('select count(*) from keyword_from_xml where keyword not like ""')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args()
    sql = 'select * from keyword_from_xml order by id limit {}, {}' \
        .format(offset, per_page)
    g.cur.execute(sql)
    keywords = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='对话',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('keyword.html', keywords=keywords,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           active_url='keywords-page-url',
                           )


@app.route('/extends/', defaults={'page': 1})
@app.route('/extends', defaults={'page': 1})
@app.route('/eextends/page/<int:page>/')
@app.route('/extends/page/<int:page>')
def extends(page):
    g.cur.execute('select count(*) from extend_from_xml where item not like ""')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args()
    sql = 'select * from extend_from_xml where item not like "" order by id limit {}, {}' \
        .format(offset, per_page)
    g.cur.execute(sql)
    extends = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='对话',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('extend.html', extends=extends,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           active_url='extends-page-url',
                           )

@app.route('/keyword/search/', methods=['GET', 'POST'])
@app.route('/keyword/search', methods=['GET', 'POST'])
def keyword_search():
    if request.method == 'POST':
        print(request.form.get('keyword'))
        sql = 'select count(*) from keyword_from_xml where keyword like ?'
        args = ('%{}%'.format(request.form.get('keyword')),)
        g.cur.execute(sql, args)
        total = g.cur.fetchone()[0]
        page, per_page, offset = get_page_args()
        sql = 'select * from keyword_from_xml where keyword like ? order by id limit {}, {}' \
            .format(offset, per_page)
        g.cur.execute(sql, args)
        keywords = g.cur.fetchall()
        pagination = get_pagination(page=page,
                                    per_page=per_page,
                                    total=total,
                                    record_name='对话',
                                    format_total=True,
                                    format_number=True,
                                    )
        return render_template('keyword.html', keywords=keywords,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               active_url='keywords-page-url',
                               )
    return render_template('keyword-search.html')

@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sql = 'select count(*) from knowledge_from_xml where question like ? '
        args = ('%{}%'.format(request.form.get('keyword')),)
        g.cur.execute(sql, args)
        total = g.cur.fetchone()[0]

        page, per_page, offset = get_page_args()
        sql = 'select * from knowledge_from_xml where question like ? order by id limit {}, {}'
        g.cur.execute(sql.format(offset, per_page), args)
        knowledges = g.cur.fetchall()
        pagination = get_pagination(page=page,
                                    per_page=per_page,
                                    total=total,
                                    record_name='对话',
                                    )
        return render_template('knowledge.html', knowledges=knowledges,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               )
    return render_template('knowledge-search.html', search=search, )


@app.route('/add', methods=['GET', 'POST'])
@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        g.cur.execute('insert into knowledge_from_xml (question,answer) values (?,?)', (request.form['question'],
                                                                                        request.form['answer']))
        g.conn.commit()
        sql = 'select count(*) from knowledge_from_xml where question like ?'
        args = ('%{}%'.format(request.form['question']),)
        g.cur.execute(sql, args)
        total = g.cur.fetchone()[0]

        page, per_page, offset = get_page_args()
        sql = 'select * from knowledge_from_xml where question like ? limit {}, {}'
        g.cur.execute(sql.format(offset, per_page), args)
        knowledges = g.cur.fetchall()
        pagination = get_pagination(page=page,
                                    per_page=per_page,
                                    total=total,
                                    record_name='对话',
                                    )
        return render_template('knowledge.html', knowledges=knowledges,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               )
    return render_template('knowledge-add.html')


@app.route('/dialog', methods=['GET', 'POST'])
@app.route('/dialog/', methods=['GET', 'POST'])
def dialog():
    if request.method == 'POST':
        sql = 'select count(*) from knowledge_from_xml where question like ? '
        args = ('%{}%'.format(request.form.get('question')),)
        g.cur.execute(sql, args)
        total = g.cur.fetchone()[0]

        page, per_page, offset = get_page_args()
        sql = 'select * from knowledge_from_xml where question like ? limit {}, {}'
        g.cur.execute(sql.format(offset, per_page), args)
        knowledges = g.cur.fetchall()
        pagination = get_pagination(page=page,
                                    per_page=per_page,
                                    total=total,
                                    record_name='对话',
                                    )
        return render_template('knowledge.html', knowledges=knowledges,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               )
    return render_template('dialog.html')


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')


def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', '对话')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )


@click.command()
@click.option('--port', '-p', default=5000, help='listening port')
def run(port):
    app.run(debug=True, port=port, host='0.0.0.0')


if __name__ == '__main__':
    run()
