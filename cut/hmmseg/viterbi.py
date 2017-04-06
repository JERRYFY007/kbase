# -*- coding: UTF-8 -*-
"""
    Hidden Markov Model--Vibiter algorithm for Chinese sentence segmentation
    @author: Yigoss.Panyi
    @date: 2014-6-7
"""
MIN_FLOAT = -3.14e100
PrevStatus = {
    'B': ('E', 'S'),
    'M': ('M', 'B'),
    'S': ('S', 'E'),
    'E': ('B', 'M')
}

from hmmseg import prob_start, prob_trans, prob_emit

start_P, trans_P, emit_P = prob_start.P, prob_trans.P, prob_emit.P


def viterbi(obs, states, start_p=start_P, trans_p=trans_P, emit_p=emit_P):
    '''
    Viterbi algorithm
    Parameters:
        obs: The obeserve value, which are the words in the sentence
        states: Hidden states, which stand for a word should be the begin(B) of the segmentation,
                Middle(M) of the segmentation, end(E) of the segmentation and stay single(S).
        start_p: The initialized probabilities, which stands for in step 0 the state's probabilities
        trans_p: The transmision matrix(state i to state j)
        emit_p: The confusion matrix(state i to obs k)
    '''
    V = [{}]  # tabular
    path = {}
    for y in states:  # init
        V[0][y] = start_p[y] + emit_p[y].get(obs[0], MIN_FLOAT)
        path[y] = [y]
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            em_p = emit_p[y].get(obs[t], MIN_FLOAT)
            (prob, state) = max([(V[t - 1][y0] + trans_p[y0].get(y, MIN_FLOAT) + em_p, y0) for y0 in PrevStatus[y]])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath

    (prob, state) = max([(V[len(obs) - 1][y], y) for y in ('E', 'S')])

    return (prob, path[state])


def gen_seg_viterbi(sentence):
    global emit_P
    prob, pos_list = viterbi(sentence, ('B', 'M', 'E', 'S'), start_P, trans_P, emit_P)
    # print("The maximum pro : %f" %(prob))
    begin, next = 0, 0
    # print pos_list, sentence
    for i, char in enumerate(sentence):
        pos = pos_list[i]
        if pos == 'B':
            begin = i
        elif pos == 'E':
            yield sentence[begin:i + 1]
            next = i + 1
        elif pos == 'S':
            yield char
            next = i + 1
    if next < len(sentence):
        yield sentence[next:]
