# -*- coding: UTF-8 -*-
'''
'''
import pyexcel_xlsx


# 判断该字符是否是中文字符（不包括中文标点）
def isChineseChar(charater):
    return 0x4e00 <= ord(charater) < 0x9fa6


# 判断是否是ASCII码
def isASCIIChar(ch):
    import string
    if ch in string.whitespace:
        return False
    if ch in string.punctuation:
        return False
    return ch in string.printable


def gen_custom_dict(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            dictionary_seg[word] = line
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def gen_dict(dictfile):
    print("Building dictionary...")
    dictionary_seg = {}
    with open(dictfile, "r", encoding='utf-8') as f:
        for line in f:
            word, freq = line.strip().split()
            dictionary_seg[word] = int(freq)
    f.close()
    print("The volumn of dictionary: %d" % (len(dictionary_seg)))
    return dictionary_seg


def mmcut(sentence, custom_dict, wordsdict, RMM=True):
    # sentence = sentence.strip()
    # print (sentence)
    result_s = ""
    s_length = len(sentence)
    english_word = ""
    if not RMM:
        result_s = "["
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if w_length == 1:
                    print(word)
                    # result_s += word + "/"
                    sentence = sentence[w_length:]
                    break
                elif word in custom_dict :
                    result_s += word + "]["
                    sentence = sentence[w_length:]
                    break
                elif word in wordsdict :
                    result_s += word + "]["
                    sentence = sentence[w_length:]
                    break
                else:
                    while w_length > 0:
                        if isASCIIChar(word[0]):
                            english_word = english_word+ str(word[0])
                            word = word[1:]
                            sentence = sentence[1:]
                            w_length = len(word)
                        else:
                            if english_word:
                                result_s += english_word + "]["
                                english_word = ""
                            break
                    word = word[:w_length - 1]
                w_length = w_length - 1
            s_length = len(sentence)
        s_length = len(result_s)
        result_s = result_s[:s_length - 1]
    else:
        result_s = ""
        while s_length > 0:
            word = sentence
            w_length = len(word)
            while w_length > 0:
                if w_length == 1:
                    print(word)
                    # result_s = word + "][" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in custom_dict:
                    result_s = word + "][" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                elif word in wordsdict:
                    result_s = word + "][" + result_s
                    sentence = sentence[:s_length - w_length]
                    break
                else:
                    while w_length > 0:
                        if isASCIIChar(word[-1]):
                            english_word = str(word[-1]) + english_word
                            word = word[:-1]
                            sentence = sentence[:-1]
                            w_length = len(word)
                        else:
                            if english_word:
                                result_s = english_word + "][" + result_s
                                english_word = ""
                            break
                    word = word[1:]
                w_length = w_length - 1
            s_length = len(sentence)
        result_s = "[" + result_s
        s_length = len(result_s)
        result_s = result_s[:s_length-1]+"\n"
    return result_s

excel_filename = 'IT知识库20170509.xlsx'

if __name__ == "__main__":
    wordsdict = gen_dict("../dict/jieba.word.freq.dic")
    custom_dict = gen_custom_dict("dict/custom.dic")
    workbook = pyexcel_xlsx.get_data(excel_filename)
    print(workbook)
    booksheet = workbook.sheet_by_name('Sheet0')
    desfmm = open('../it_fmm.txt', 'w', encoding='utf-8')
    desrmm = open('../it_rmm.txt', 'w', encoding='utf-8')

    i = 0
    for row in range(booksheet.nrows):
        cel = booksheet.cell(row, 0)
        it_question = cel.value
        try:
            val = cel.value
        except:
            pass
        # print(row_data, row_data[0], row_data[1], row_data[2], row_data[3])
        if it_question == "标准问题":
            continue
        i += 1
        if it_question != "":
            qa_id = qa_id + 1

    with open('../IT.txt', 'r', encoding='utf-8') as src:
        for inline in src:
            wordsegfmm = ''.join(mmcut(inline, custom_dict, wordsdict, RMM=False))
            wordsegrmm = ''.join(mmcut(inline, custom_dict, wordsdict))
            desfmm.write(wordsegfmm + "\n")
            desrmm.write(wordsegrmm)
    desfmm.close()
    desrmm.close()
