# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:pyltp0.1.py
# @time:2017/6/18 0018 22:27
# -*- coding: utf-8 -*-
# 分句
from pyltp import SentenceSplitter

sents = SentenceSplitter.split('元芳你怎么看？我就趴窗口上看呗！')  # 分句
print('\n'.join(sents))

import os

LTP_DATA_DIR = '/ltp_data'  # ltp模型目录的路径
# 分词
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
from pyltp import Segmentor

segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型
words = segmentor.segment('元芳你怎么看')  # 分词
print('\t'.join(words))
input_txt = '查询5月份的电费'
words = segmentor.segment(input_txt)
print('\t'.join(words))
segmentor.release()  # 释放模型

# 词性标注
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
from pyltp import Postagger

postagger = Postagger()  # 初始化实例
postagger.load(pos_model_path)  # 加载模型
words = ['元芳', '你', '怎么', '看']  # 分词结果
postags = postagger.postag(words)  # 词性标注
print('词性标注:')
print('\t'.join(postags))
postagger.release()  # 释放模型

# 命名实体识别
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
from pyltp import NamedEntityRecognizer

recognizer = NamedEntityRecognizer()  # 初始化实例
recognizer.load(ner_model_path)  # 加载模型
words = ['元芳', '你', '怎么', '看']
postags = ['nh', 'r', 'r', 'v']
netags = recognizer.recognize(words, postags)  # 命名实体识别
print('命名实体识别:')
print('\t'.join(netags))
recognizer.release()  # 释放模型

# 依存句法分析
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
from pyltp import Parser

parser = Parser()  # 初始化实例
parser.load(par_model_path)  # 加载模型
words = ['元芳', '你', '怎么', '看']
postags = ['nh', 'r', 'r', 'v']
arcs = parser.parse(words, postags)  # 句法分析
print('依存句法分析:')
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
parser.release()  # 释放模型

# 语义角色标注
srl_model_path = os.path.join(LTP_DATA_DIR, 'srl')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
from pyltp import SementicRoleLabeller

labeller = SementicRoleLabeller()  # 初始化实例
labeller.load(srl_model_path)  # 加载模型
words = ['元芳', '你', '怎么', '看']
postags = ['nh', 'r', 'r', 'v']
netags = ['S-Nh', 'O', 'O', 'O']
# arcs 使用依存句法分析的结果
roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
# 打印结果
print('语义角色标注:')
for role in roles:
    print(role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
labeller.release()  # 释放模型
