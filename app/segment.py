# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:view.py
# @time:2017/3/29
from flask import render_template, request
from app import app


class Segmentation:
    def __init__(self):
        # 新建列表存放分词词典读出来的词
        d = []
        with open('sogou.dic_utf8', 'r', encoding='utf-8') as fd:
            flists = fd.readlines()
            for flist in flists:
                s = flist.split()
                d.append(s[0])
            # 将列表转换为元祖
            self.word_set = tuple(d)
        d = []
        with open('keywordxml.dic', 'r', encoding='utf-8') as fd:
            flists = fd.readlines()
            for flist in flists:
                s = flist.split()
                d.append(s[0])
            # 将列表转换为元祖
            self.keyword = tuple(d)

    def set_sentence(self, sentence):
        self.sentence = sentence
        self.seg_result_dict = {}  # 初始化划分结果

    def get_result_dict(self):
        """
        获得分词结果字典
        :return:
        """
        return self.seg_result_dict

    def mm_seg(self, max_len=6):
        """
        使用正向最大匹配法划分词语
        :param max_len: int 最大词长 默认为6
        """
        cur = 0  # 表示分词的位置
        seg_result = []
        sen_len = self.sentence.__len__()  # 句子的长度
        while cur < sen_len:
            l = None
            for l in range(max_len, 0, -1):
                if self.sentence[cur: cur + l] in self.keyword:
                    break
                elif self.sentence[cur: cur + l] in self.word_set:
                    break
            seg_result.append(self.sentence[cur: cur + l])
            cur += l
        self.seg_result_dict['MM'] = seg_result

    def rmm_seg(self, max_len=6):
        """
        使用逆向最大匹配法划分词语
        :param max_len: int 最大词长 默认为6
        """
        sen_len = self.sentence.__len__()  # 句子的长度
        seg_result = []
        cur = sen_len  # 表示分词的位置
        while cur > 0:
            l = None
            if max_len > cur:
                max_len = cur
            for l in range(max_len, 0, -1):
                if self.sentence[cur - l: cur] in self.word_set:
                    break
            seg_result.insert(0, self.sentence[cur - l: cur])
            cur -= l
        self.seg_result_dict['RMM'] = seg_result


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
        analyse = []
        return render_template('segment.html', sentence=segment, segmented=segmented, analyse=analyse)
    return render_template('segment.html')