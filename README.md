# KBase 客服知识库维护工具

> 使用python语言、flask web框架、 SQLite3数据库等技术编写

> 需要flask、sqlite3、flask_paginate、xlrd、xlsxwriter等库支持

### 目前实现以下功能：
- 浏览标准问题及标准答案
- 查找标准问题
- 增加标准问题及标准答案

### 计划实现的功能：
- 编辑标准问题及标准答案
- 新增、编辑扩展问题
- 新增、编辑分支问题

### 目录结构

### 使用
> 程序及数据文件在kbase主目录下

> kbase0.1.py为主程序，在本机启动后使用浏览器打开[http://127.0.0.1:5000](http://127.0.0.1:5000)即可

> xlsx2sql.py 将 “知识库.xlsx” 转换为SQLite3数据库 “kbase.db” 

> sql2xlsx 可将SQLite3数据库 “kbase.db” 转换为excel文件 “kbase.xlsx”