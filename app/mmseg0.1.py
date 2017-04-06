# -*- coding: UTF-8 -*-
'''
	The forward Maximum Match and Reverse Maximum Match for Chinese sentence segmentation
	@author: Yigoss.Panyi
	@date: 2014-6-7
'''
import hmmseg

def gen_dict(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, freq, _ = line.strip().split()
            dictionary_seg[word] = int(freq)
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def mmcut(sentence, wordsdict, RMM=True):
    # print (sentence)
    result_s = ""
    s_length = len(sentence)
    if not RMM:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict or w_length == 1:
                    result_s += word + "/"
                    sentence = sentence[w_length:]
                    break
                else:
                    word = word[:w_length - 1]
                    # print(word)
                w_length = w_length - 1
            s_length = len(sentence)
    else:
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if word in wordsdict or w_length == 1:
                    result_s = word + "/" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
    return result_s


if __name__ == "__main__":
    wordsdict = gen_dict("dict/dict.txt")
    deshmm = open('../question_hmm.txt', 'w', encoding='utf-8')
    desfmm = open('../question_fmm.txt', 'w', encoding='utf-8')
    desrmm = open('../question_rmm.txt', 'w', encoding='utf-8')
    with open('../question.txt', 'r', encoding='utf-8') as src:
        for inline in src:
            wordseghmm = ''.join(hmmseg.cut(inline))
            wordsegfmm = ''.join(mmcut(inline, wordsdict, RMM=False))
            wordsegrmm = ''.join(mmcut(inline, wordsdict))
            deshmm.write(wordseghmm)
            desfmm.write(wordsegfmm)
            desrmm.write(wordsegrmm)
    src.close()
