# encoding: utf-8
from __future__ import division
import numpy as np

def count_fea(sub):
    ''' count the number of pattern such as [[pattern],[0,0,1]] '''
    pattern_num = []
    cal_seq = True
    sub1 = sub[:,::-1].T
    rank = np.lexsort(sub1)
    subsorted = sub[rank] # use for sort according to row but save the Integrity of rows
    if cal_seq:
        rank_reshape = np.reshape(rank,(len(rank),1))
        subsorted = np.concatenate([subsorted,rank_reshape],axis=1)
        count = 0
        while count < len(subsorted):
            n = 0
            for i in subsorted[count:]:
                if not (subsorted[count] - i).any():
                    n += 1
            # print n
            pattern_num.append(
                [subsorted[count, :-2], subsorted[count, -2], n, list(subsorted[count:count+n,-1])]) # append pattern and number for example [patter,num]
            count += n
        return pattern_num

def pattern_dict_func(pattern_num,c):
    '''calculate the pattern for different class: {(1, 2, 1, 1): [1, 1], (2, 1, 1, 1): [1, 0], (2, 1, 1, 2): [0, 1]}'''
    pattern_dict = {}
    for i in range(len(pattern_num)):
        pattern = tuple(pattern_num[i][0])
        b = [0] * c
        if pattern not in pattern_dict:
            pattern_dict[pattern] = b # The first is pattern number for different classes; the second is the no. of pattern (1, 2, 1, 1): [[1, 1],[(1),(2)]]
        # print pattern_num[i][1]
        pattern_dict[pattern][pattern_num[i][1]-1] += pattern_num[i][2]
    return pattern_dict

def check_removal(pattern_num,pattern_dict,sigma=0.2):
    '''check the the removal objects'''
    singular_pattern = []
    removal = []
    for i in pattern_dict:
        distribution = np.array(pattern_dict[i]) / sum(pattern_dict[i])
        if np.any((distribution < sigma) & (distribution>0)):
            label = np.where((distribution < sigma) & (distribution>0))[0]
            list_i = list(i)
            singular_pattern = singular_pattern + [list_i+[j+1] for j in label]
    pattern_num2 = np.array([np.append(pattern_num[i][0],pattern_num[i][1]) for i in range(len(pattern_num))])
    for i in range(len(singular_pattern)):
        mask = pattern_num2 == singular_pattern[i]
        for j in range(len(mask)):
            if np.all(mask[j]):
                removal = removal+pattern_num[j][-1]
    return removal

def ConsisCal(X,y,rem=True,sigma=0.2):
    '''X: Data without labels
       Y: labels
       c: classes
    '''
    row = len(X)
    c = len(np.unique(y))
    sigma=sigma
    print ('inner function',sigma)
    sub = np.column_stack((X,y))
    pattern_num = count_fea(sub)
    # print pattern_num
    pattern_dict = pattern_dict_func(pattern_num,c)
    # print pattern_dict
    if rem:
        removal = check_removal(pattern_num,pattern_dict,sigma=sigma)
        # print 'removal set length',len(removal)
        InconNum = 0
        for _,value in pattern_dict.items():
            InconNum += sum(value) - max(value)
        InconRate = InconNum/row
        return InconRate,removal
    else:
        InconNum = 0
        for _, value in pattern_dict.items():
            InconNum += sum(value) - max(value)
        InconRate = InconNum / row
        return InconRate

if __name__ == '__main__':

    a = [[1, 2, 1,1],[2, 1, 1,2],[1, 2, 1,1],[2, 1, 1,1]]
    y = [1, 2, 2, 1]
    print (ConsisCal(a, y))

