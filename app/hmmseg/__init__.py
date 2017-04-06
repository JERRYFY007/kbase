# -*- coding: UTF-8 -*-
'''
	Hidden Markov Model for Chinese sentence segmentation
	@author: Yigoss.Panyi
	@date: 2014-6-7
'''
from hmmseg.viterbi import gen_seg_viterbi
import re


def cut(sentence):
    """
	Call the viterbi Algorithm and do the segmentation,cache the result in a cache dictionary file
	Parameters:
		sentence: The String to be segmented
	"""
    unlog_word_cache = open("dict/dict.txt.temp", "w")
    # sentence
    re_han = re.compile("([\u4E00-\u9FA5a-zA-Z0-9+#&\._]+)", re.U)
    re_skip = re.compile("(\r\n|\s)", re.U)
    re_eng = re.compile("([a-zA-Z0-9+#&\._]+)", re.U)
    blocks = re_han.split(sentence)
    resultls = []
    # result = ""
    for statement in blocks:
        if (len(statement) == 0):
            continue
        if (re_han.match(statement)):
            eng_blocks = re_eng.split(statement)
            for blk in eng_blocks:
                if (len(blk) == 0):
                    continue
                if (re_eng.match(blk)):
                    # result += "/" + blk
                    resultls.append(blk)
                else:
                    seg_result = gen_seg_viterbi(blk)
                    resultls.extend(seg_result)
                    # result += "/".join(seg_result)
        else:
            # result += "/" + statement + "/"
            resultls.append(statement)
    # print resultls
    for w in resultls:
        if (len(w) > 1):
            unlog_word_cache.write("%s %d %s\n" % (w, 5, 'uk'))
    unlog_word_cache.close()
    # return result
    return "/".join(resultls)
