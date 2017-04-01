from __future__ import unicode_literals
from flask import render_template, g, request,redirect,url_for
from app import app



@app.route('/knowledge/view', defaults={'id': 1}, methods=['GET'])
@app.route('/knowledge/view/', defaults={'id': 1}, methods=['GET'])
@app.route('/knowledge/view/<int:id>/')
@app.route('/knowledge/view/<int:id>')
def knowledge_view(id):
    if request.method == 'GET' and id :
        sql = 'select * from knowledge_from_xml where id = {}'.format(id)
        g.cur.execute(sql)
        knowledges = g.cur.fetchall()
        return render_template('knowledge-view.html', knowledges = knowledges, )


@app.route('/knowledge/edit', defaults={'id': 1})
@app.route('/knowledge/edit/', defaults={'id': 1})
@app.route('/knowledge/edit/<int:id>/')
@app.route('/knowledge/edit/<int:id>')
def knowledge_edit(id):
    if request.method == 'GET' and id :
        sql = 'select * from knowledge_from_xml where id = {}'.format(id)
        g.cur.execute(sql)
        knowledges = g.cur.fetchall()
    return render_template('knowledge-edit.html', knowledges = knowledges,)


@app.route('/knowledge/delete', defaults={'id': 1})
@app.route('/knowledge/delete/', defaults={'id': 1})
@app.route('/knowledge/delete/<int:id>/')
@app.route('/knowledge/delete/<int:id>')
def knowledge_delete(id):
    if request.method == 'GET' and id :
        sql = 'select * from knowledge_from_xml where id = {}'.format(id)
        g.cur.execute(sql)
        knowledges = g.cur.fetchall()
    return render_template('knowledge-delete.html', knowledges = knowledges,)


@app.route('/knowledge/add')
@app.route('/knowledge/add/')
def knowledge_add():
    if request.method == 'GET':
        return render_template('knowledge-add.html')
    return render_template('knowledge-add.html')


@app.route('/knowledge/search', defaults={'search':''})
@app.route('/knowledge/search/', defaults={'search':''})
@app.route('/knowledge/search/<search>/')
@app.route('/knowledge/search/<search>')
def knowledge_search(search):
    if request.method == 'GET' and search :
        sql = 'select * from knowledge_from_xml where id = {}'.format(search)
        g.cur.execute(sql)
        knowledges = g.cur.fetchall()
        return render_template('knowledge-search.html', knowledges=knowledges, )
    else:
        return render_template('knowledge-search.html')


@app.route('/keyword/list/<int:id>/')
@app.route('/keyword/list/<int:id>')
@app.route('/keyword/view/<int:id>/')
@app.route('/keyword/view/<int:id>')
@app.route('/keyword/edit/<int:id>/')
@app.route('/keyword/edit/<int:id>')
@app.route('/keyword/delete/<int:id>/')
@app.route('/keyword/delete/<int:id>')
@app.route('/keyword/update/<int:id>/')
@app.route('/keyword/update/<int:id>')
def keyword_list(id):
    if request.method == 'GET' and id :
        sql = 'select * from keyword_from_xml where id = {}'.format(id)
        g.cur.execute(sql)
        keywords = g.cur.fetchall()
    return render_template('keyword-list.html', keywords = keywords,)


@app.route('/keyword/add/', methods=['GET', 'POST'])
@app.route('/keyword/add', methods=['GET', 'POST'])
def keyword_add():
    if request.method == 'POST' :
        print(request.form.get('keyword'))
        sql = 'select * from keyword_from_xml where keyword like ?'
        args = ('%{}%'.format(request.form.get('keyword')),)
        g.cur.execute(sql, args)
        keywords = g.cur.fetchall()
        return render_template('keyword-search.html',keywords = keywords)
    return render_template('keyword-search.html')


@app.route('/extend/list/<int:id>/')
@app.route('/extend/list/<int:id>')
@app.route('/extend/view/<int:id>/')
@app.route('/extend/view/<int:id>')
@app.route('/extend/edit/<int:id>/')
@app.route('/extend/edit/<int:id>')
@app.route('/extend/delete/<int:id>/')
@app.route('/extend/delete/<int:id>')
@app.route('/extend/update/<int:id>/')
@app.route('/extend/update/<int:id>')
def extend_list(id):
    if request.method == 'GET' and id :
        sql = 'select * from extend_from_xml where id = {}'.format(id)
        g.cur.execute(sql)
        extends = g.cur.fetchall()
    return render_template('extend-list.html', extends = extends,)


@app.route('/extend/add/', methods=['GET', 'POST'])
@app.route('/extend/add', methods=['GET', 'POST'])
@app.route('/extend/search/', methods=['GET', 'POST'])
@app.route('/extend/search', methods=['GET', 'POST'])
def extend_add():
    if request.method == 'GET' :
        return render_template('extend-add.html')
    return render_template('extend-add.html')


