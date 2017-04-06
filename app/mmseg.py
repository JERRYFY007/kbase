# -*- coding: UTF-8 -*-
'''
	The forward Maximum Match and Reverse Maximum Match for Chinese sentence segmentation
	@author: Yigoss.Panyi
	@date: 2014-6-7
'''
import sys
import hmmseg

# reload(sys)
# sys.setdefaultencoding('utf-8')


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
    '''
	Implemented the forward Maximum Match and Reverse Maximum Match
	Parameters:
		sentence: The String to be segmented
		wordsdict: Dictionary
		RMM: Whether use the Reverse Maximum Match Method
	'''

    # print sentence
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


def seg_test():
    '''
	Test the sentence segmentation
	'''
    result = mmcut("这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱中国共产党,我爱Python。爱C++。", wordsdict)
    print("Reverse Maximum Match: %s" % (result))
    result = hmmseg.cut("这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱中国共产党,我爱Python。爱C++。")
    print("HMM segmentation: %s" % (result))

    result = mmcut("在语音识别中这种类型的问题发生在当一大堆数目的马尔科夫模型被使用，并且每一个模型都对一个特殊的单词进行建模时。", wordsdict)
    print("Reverse Maximum Match: %s" % (result))
    result = mmcut("在语音识别中这种类型的问题发生在当一大堆数目的马尔科夫模型被使用，并且每一个模型都对一个特殊的单词进行建模时。", wordsdict, RMM=False)
    print("Forward Maximum Match: %s" % (result))
    result = hmmseg.cut("在语音识别中这种类型的问题发生在当一大堆数目的马尔可夫模型被使用，并且每一个模型都对一个特殊的单词进行建模时。")
    print("HMM segmentation: %s" % (result))

    result = mmcut("研究生命起源", wordsdict, RMM=False)
    print("Reverse Maximum Match: %s" % (result))

    result = mmcut("我来到北京清华大学", wordsdict, RMM=True)
    print("Reverse Maximum Match: %s" % (result))
    result = hmmseg.cut("我来到北京清华大学")
    print("HMM segmentation: %s" % (result))
    result = hmmseg.cut("我来到北京清华大学")
    print("HMM segmentation %s" % (result))

    result = mmcut("你现在应该去幼儿园了。", wordsdict)
    print("Reverse Maximum Match: %s" % (result))
    result = hmmseg.cut("你现在应该去幼儿园了。")
    print("HMM segmentation: %s" % (result))

    result = mmcut("李天意愿意捐款", wordsdict, RMM=False)
    print("HMM segmentation: %s" % (result))
    result = hmmseg.cut("射洪县青岗镇是我的美丽的故乡")
    print("HMM segmentation: : %s" % (result))
    result = hmmseg.cut("侵华日军南京大屠杀遇难同胞纪念馆")
    print("HMM segmentation: %s" % (result))

    result = hmmseg.cut("南京市长江大桥")
    print("HMM segmentation: %s" % (result))
    result = mmcut("南京市长江大桥", wordsdict, RMM=False)
    print("Forward Maximum Match: %s" % (result))
    result = mmcut("南京市长江大桥", wordsdict)
    print("Reverse Maximum Match: %s" % (result))


if __name__ == "__main__":
    wordsdict = gen_dict("dict/dict.txt")
    seg_test()
