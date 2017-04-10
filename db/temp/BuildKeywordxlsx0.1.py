# -*- coding: utf-8 -*-
import re
import xlrd

# 新建列表存放分词词典读出来的词
d = []
with open('sogou.dic_utf8', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        s = flist.split()
        d.append(s[0])
    # 将列表转换为元祖
    lexicon = tuple(d)

excel_filename = '知识库.xlsx'
workbook = xlrd.open_workbook(excel_filename)
booksheet = workbook.sheet_by_name('Sheet0')
# Process
tmp, kw_data, new_keyword = [], [], []
tu_new_keyword, tu_tmp = (), ()
i = 0
for row in range(booksheet.nrows):
    row_data = []
    for col in range(booksheet.ncols):
        cel = booksheet.cell(row, col)
        val = cel.value
        try:
            val = cel.value
        except:
            pass
        row_data.append(val)
    # print(row_data, row_data[0], row_data[1], row_data[2], row_data[3])
    if row_data[0] == "标准问题":
        continue
    i = i + 1
    if row_data[0] != "":
        continue
    else:
        temp_extend = re.sub(r'[[]', '', row_data[1])
        extends = re.split(r'[]]', temp_extend)
        extends.pop(-1)
        for extend in extends:
            if re.search(r'[|]', extend) is None:
                if extend in tu_tmp or extend in tu_new_keyword:
                    continue
                elif extend in lexicon:
                    tmp.append(extend + '\n')
                    tu_tmp = tuple(tmp)
                else:
                    new_keyword.append(extend + '\n')
                    tu_new_keyword = tuple(new_keyword)
            else:
                synonyms = re.split(r'[|]', extend)
                sy_id = 0
                for synonym in synonyms:
                    sy_id = sy_id + 1
                    if len(synonyms) > sy_id:
                        if synonym in tu_tmp or synonym in tu_new_keyword:
                            continue
                        elif synonym in lexicon:
                            tmp.append(synonym + '\n')
                            tu_tmp = tuple(tmp)
                        else:
                            new_keyword.append(synonym + '\n')
                            tu_new_keyword = tuple(new_keyword)
print('Process keyword: ', i)

print("去重复前的词数为:", len(tmp), len(new_keyword))
set_data = set(tmp)  # 去重复
last_data = list(set_data)  # set转换成list, 否则不能索引
set_new_keyword = set(new_keyword)
last_new_keyword = list(set_new_keyword)
print("去除重复后总词数为:", len(last_data), len(last_new_keyword))

open('keywordxlsx.tmp', 'w', encoding='utf8').writelines(last_data)
open('newkeywordxlsx.tmp', 'w', encoding='utf8').writelines(last_new_keyword)
print("最终词表文件建立完成! (keywordxlsx.tmp)")


