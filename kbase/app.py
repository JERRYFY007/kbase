# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:kbase0.2.py
# @time:2017/3/14 0014 15:36

from __future__ import unicode_literals
from flask import Flask, render_template, g, current_app, request
from flask_paginate import Pagination, get_page_args
from Segmentation import Segmentation
import sqlite3
import click

click.disable_unicode_literals_warning = True
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db_filename = 'knowledge.db'


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
    return render_template('index.html')


@app.route('/knowledges/', defaults={'page': 1})
@app.route('/knowledges', defaults={'page': 1})
@app.route('/knowledges/page/<int:page>/')
@app.route('/knowledges/page/<int:page>')
def knowledges(page):
    g.cur.execute('select count(*) from knowledge_from_xml where question not like ""')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_args()
    sql = 'select question,answer from knowledge_from_xml where question not like "" order by id limit {}, {}' \
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
    sql = 'select qa_id,ex_id,keyword,importance,synonym from keyword_from_xml order by id limit {}, {}' \
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
    sql = 'select qa_id,ex_id,item,omit,synonym from extend_from_xml where item not like "" order by id limit {}, {}' \
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


@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sql = 'select count(*) from knowledge_from_xml where question like ? '
        args = ('%{}%'.format(request.form.get('keyword')),)
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
    # return redirect(url_for('search'))
    return render_template('search.html', search=search, )


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
    # return redirect(url_for('add'))
    return render_template('add.html')


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

    # dialog = g.cur.fetchall()
    #       print(dialog)
    #      return render_template('dialog.html', dialog = dialog)
    return render_template('dialog.html')


@app.route('/segment', methods=['GET', 'POST'])
@app.route('/segment/', methods=['GET', 'POST'])
def segment():
    if request.method == 'POST':
        segment = request.form.get('sentence')
        print(segment)
        seg = Segmentation()
        seg.set_sentence(segment)
        seg.mm_seg()  # MM
        seg.rmm_seg()  # RMM
        seg.max_probability_seg()  # 最大概率分词
        r = seg.get_result_dict()  # 获得分词结果字典
        # print '|'.join(r['MM'])
        # print '|'.join(r['RMM'])
        # print '|'.join(r['MP'])
        #seg.print_result()  # 将分词结果输出
        segmented = []
        segmented.append('MM:')
        segmented.append('/'.join(r['MM']))
        segmented.append('\n')
        segmented.append('RMM:')
        segmented.append('/'.join(r['RMM']))
        segmented.append('\n')
        segmented.append('MP:')
        segmented.append('/'.join(r['MP']))
        segmented.append('\n')
        return render_template('segment.html', segmented=segmented)
    return render_template('segment.html')


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
    app.run(debug=True, port=port)


if __name__ == '__main__':
    run()
