# -*- coding:utf-8 -*-
# @author:Eric Luo
# @file:qa.py
# @time:2017/6/8
#

from lxml import etree

from .segment import *


# 预加载字典文件
def load_dataframe():
    # 读取并生成关键词和全局同义词字典
    print("Building keywords dictionary...")
    dict_keyword = {}
    with open("app/dict/keyword.dict", encoding='utf8') as f:
        for line in f:
            (val, imp) = line.strip().split(',')
            dict_keyword[val] = imp
    print("Dict Keyword:", len(dict_keyword))

    # 读取并生成局部同义词字典
    print("Building local synonym dictionary...")
    dict_synonym = {}
    with open("app/dict/extend.dict", encoding='utf8') as f:
        for line in f:
            word, item = line.strip().lower().split(',')
            if item != 'Item':
                dict_synonym[word] = item
    print("Dict local synonym: %d" % (len(dict_synonym)))

    # 读取并生成问答扩展问字典
    print("Building extends dictionary...")
    dict_extend = {}
    with open("app/dict/extend.dict", encoding='utf8') as f:
        for line in f:
            dict_item = {}
            (qa_ex_id, item) = line.strip().split(',')
            if item == "Item":
                continue
            # print(qa_ex_id, item)
            items = item.split(';')
            items.pop(-1)
            # print(items)
            sy = []
            for keyword in items:
                # print(keyword)
                sy.append(keyword.split('|'))
                dict_item[keyword] = sy
            # print("Extend:", sy)
            dict_extend[qa_ex_id] = sy
    print("Dict extend: ", len(dict_extend))
    return dict_keyword, dict_synonym, dict_extend


# 问句分词，最大匹配算法，缺省正相匹配
def fmmcut(sentence, dict_kw, dict_local_sy, FMM=True):
    result_s = []
    sentence = sentence.lower()
    s_length = len(sentence)
    if FMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                # 关键词及全局同义词切分
                if word in dict_kw:
                    result_s.append("@" + word + "," + str(dict_kw.get(word)))
                    sentence = sentence[w_length:]
                    break
                # 局部同义词切分
                elif word in dict_local_sy:
                    print("Find a local synonym word: ", word)
                    result_s.append("#" + word + "," + dict_local_sy.get(word))
                    sentence = sentence[w_length:]
                    break
                # 切分至单字
                elif w_length == 1:
                    result_s.append(word)
                    sentence = sentence[w_length:]
                    break
                else:
                    word = word[:w_length - 1]
                w_length = w_length - 1
            s_length = len(sentence)
    else:  # 反向最大匹配，暂不使用
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in dict_kw:
                    result_s.insert(0, ("@" + word + "," + str(dict_kw.get(word))))
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in dict_local_sy or w_length == 1:
                    result_s.insert(0, word)
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
    return result_s


# 加载问答对
def load_qa(xml_filename):
    print("Building Question, Answer, Branch Dict...")
    # Process knowledge.xml
    tree = etree.parse(xml_filename)
    root = tree.getroot()
    dict_question, dict_answer, dict_branch = {}, {}, {}
    qa_id = 0
    for knowledge in root:
        qa_id = qa_id + 1
        br_id = 0
        for field in knowledge:
            if field.tag == "question":
                dict_question[qa_id] = field.text
            if field.tag == "answer":
                dict_answer[qa_id] = field.text
            if field.tag == "branch":
                br_id += 1
                dict_branch[str(qa_id) + ':' + str(br_id)] = field.text
    print("The volumn of Question, Answer, Branch Dict:", len(dict_question), len(dict_answer), len(dict_branch))
    return dict_question, dict_answer, dict_branch


def get_qa(items):
    question, answer, branch = [], [], []
    if len(items) > 4:
        max5 = 4
    else:
        max5 = len(items)
    for j in range(max5):
        qa_id = items[j]
        if int(qa_id) in dict_question:
            # print("Find question & answer!")
            question.append(dict_question.get(int(qa_id)))
            answer.append(dict_answer.get(int(qa_id)))
            branch.append(dict_branch.get(qa_id))
    return question, answer, branch


"""
计算问句分值
* 算法说明：逐个比较keyword[]与extend.get(i)
* 1、计算该extend的最高匹配分：将其所有item根据重要性和是否可省略评分，再相加得到最高匹配分（满分）
* 2、计算keyword[]与extend的重合关键词，将重合关键词的分数相加，得到匹配分。
* 3、计算keyword[]中与extend不重合的关键词，将不重合关键词的分数相加，乘以系数，得到不匹配分
* 4、总得分 = (匹配分-不匹配分)/最高匹配分
"""


def CountPoint(dict_seg):
    best_id, best, best_extend = [''], [0.0], ['']

    with open("app/dict/extend.dict", encoding='utf8') as f:  # 可事先加载问扩展问字典，不用每次都读文件
        for line in f:
            (qa_ex_id, extends) = line.strip().split(',')
            extends = extends.strip().split(';')
            extends.pop(-1)

            point, max, match, unmatch = 0.0, 0.0, 0.0, 0.0

            # 计算扩展问的最大分，可事先计算好生成字典文件
            for extend in extends:
                max += float(dict_keyword.get(extend.strip().split('|')[0]))
                # print(qa_ex_id, extend.strip().split('|')[0], dict_keyword.get(extend.strip().split('|')[0]), max)

            for seg in dict_seg.keys():
                sucess = False
                for extend in extends:
                    items = extend.strip().split('|')
                    if seg in items:
                        match += float(dict_keyword.get(items[0]))
                        sucess = True
                        # print("Matched:", qa_ex_id, list_seg, seg, seg_point, match)
                        break
                if sucess == False:
                    unmatch += float(dict_keyword.get(seg)) * 0.3
                    # print("Unmatched:",qa_ex_id, seg, seg_point, unmatch)

            # print("qa_ex_id, match, unmatch, max:", qa_ex_id, match, unmatch, max)
            # 计算扩展问的总分point，确定是否最佳
            if max == 0 or match == 0 or match < unmatch:  # max=0代表空白扩展问；match=0代表全部不匹配；match < unmatch 代表不匹配度太高
                continue
            else:
                # 计算总分
                point = (match - unmatch) / max
                # print("qa_ex_id, point, max, match, unmatch", qa_ex_id, point, max, match, unmatch)

                if point > 0.55:
                    print("Best qa_ex_id, point, max, match, unmatch", qa_ex_id, point, max, match, unmatch)
                    # 与当前最佳分比较
                    if point >= best[0]:
                        (qa_id, _) = qa_ex_id.split(':')  # 只保留问答对序号，丢弃扩展问序号
                        # 如果问答对序号不一致才加入最佳答案
                        if qa_id not in best_id:
                            best.insert(0, point)
                            best_id.insert(0, qa_id)
                            best_extend.insert(0, extends)
        best.pop(-1)
        best_id.pop(-1)
        print('Best ID & point:', best_id, best)
    return best_id, best, best_extend


dict_keyword, dict_synonym, dict_extend = load_dataframe()  # 预加载字典文件，关键词、局部同义词、扩展问
dict_question, dict_answer, dict_branch = load_qa("app/dict/knowledge.xml")  # 预加载问答知识库问答对文件，及扩展问


@app.route('/qa', methods=['GET', 'POST'])
@app.route('/qa/', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        question = request.form.get('question')  # 从页面读取问句
        dict_seg = {}
        fmm1 = fmmcut(question, dict_keyword, dict_synonym)  # 问句分词
        for word in fmm1:
            if '@' in word:
                word, importance = word.strip().split(',')
                _, word = word.strip().split('@')
                dict_seg[word] = float(importance)
        best_id, best_point, best_extend = CountPoint(dict_seg)  # 问句分词后计算分值，返回最优
        best_questions, best_answers, branch = get_qa(best_id)  # 提取问答对
        # 问答记录至log文件中，事后分析
        app.logger.info("Question: %s", question)  # 问句记录至log文件中
        app.logger.info("Question Segmation: %s", fmm1)  # 问句分词后记录至log文件中
        app.logger.info("Best id & point: %s %s", best_id, best_point)
        app.logger.info("Best Question: %s", best_questions)
        app.logger.info("Best Answer: %s", best_answers)
        # 输出至页面
        return render_template('qa.html', qa=True, question=question, seg=dict_seg, ids=best_id, points=best_point,
                               extend=best_extend, questions=best_questions, answers=best_answers, )
    # 显示页面QA，输入问句
    return render_template('qa.html', )
