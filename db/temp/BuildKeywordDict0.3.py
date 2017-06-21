# -*- coding: utf-8 -*-

tmp = []
# Read keyword xml
with open('keywordxml.tmp', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        # print(flist)
        s = flist.split()
        # print(s[0])
        tmp.append(s[0] + '\n')
print("文件完成! (keywordxml.dict)")

# Read keyword xlsx
with open('keywordxlsx.tmp', 'r', encoding='utf-8') as fd:
    flists = fd.readlines()
    for flist in flists:
        # print(flist)
        s = flist.split()
        # print(s[0])
        tmp.append(s[0] + '\n')
print("文件完成! (keywordxlsx.dict)")

print("去重复前的词数为:", len(tmp))
set_data = set(tmp)  # 去重复
lalst_data = list(set_data)  # set转换成list, 否则不能索引
print("去除重复后总词数为:", len(lalst_data))
open('keyword.dict', 'w', encoding='utf8').writelines(lalst_data)
print("最终词表文件建立完成! (keyword.dict)")
