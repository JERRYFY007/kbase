# -*- coding: utf-8 -*-

import re
import xlrd

excel_filename = '知识库.xlsx'
workbook = xlrd.open_workbook(excel_filename)
booksheet = workbook.sheet_by_name('Sheet0')

# Process
tmp = []
kw_data = []
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
                tmp.append(extend + '\n')
                print("Add one new keyword:", extend)
print('Process keyword: ' + str(i))

print("去重复前的词数为:", len(tmp))
set_data = set(tmp)  # 去重复
lalst_data = list(set_data)  # set转换成list, 否则不能索引
print("去除重复后总词数为:", len(lalst_data))

open('keywordxlsx.dict', 'w', encoding='utf8').writelines(lalst_data)
print("最终词表文件建立完成! (keywordxlsx.dict)")


