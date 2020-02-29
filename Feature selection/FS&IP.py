# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from collections import Counter
from Con_method import ConsisCal
from sklearn.model_selection import KFold
from sklearn import tree
from sklearn.metrics import accuracy_score
from skfeature.function.information_theoretical_based import MRMR


np.set_printoptions(threshold=1000)
pd.set_option('max_colwidth',1000)
pd.set_option('display.max_rows',None)


'''The core algorithm of FS&IP.'''
def LCC(X_re,y,miu,sigma=0.2):
    m,n = X_re.shape
    G = pd.Series(range(m))
    li = 0
    ri = n - 1
    con_ri_result = ConsisCal(X_re[:,:],y,sigma=sigma)
    con_ri = con_ri_result[0]
    if con_ri > miu:
        print 'threshold is small',con_ri
        # return None
    while ri > li:
        mid = (li+ri)/2
        con_mid_result = ConsisCal(X_re[:,:-mid],y,sigma=sigma)
        con_mid = con_mid_result[0]
        # print con_mid,mid,li,ri
        if not con_mid_result[1]:
            removal = con_mid_result[1]
            instance_remain = list(set(range(len(X_re))).difference(removal))
            temp = G[~G.isin(removal)]
            X_re = X_re[instance_remain]
            y = y[instance_remain]
            G = pd.Series(range(len(instance_remain)),index=temp.index)
        if con_mid < miu:
            li = mid+1
        elif con_mid > miu:
            ri = mid-1
        else:
            return mid,G.index
    return li, G.index


if __name__ == '__main__':
    '''Read file'''
    data = []
    y = []
    with open(r'.\Open access\FS&IP\skfeature\data', 'r') as f:
        for line in f:
            if line != ' ':
                line = line.rstrip().split(',')
                data.append(line[:-1])
                y.append(line[-1])
            else:
                pass
    data = np.array(data, dtype=np.float)
    y_o = np.array(y, dtype=np.str_)

    '''Convert the class name into number which is convenient to make classification.'''
    y = []
    c = Counter(y_o)
    label = c.keys()
    category = len(label)

    labeltranform = range(1, len(label) + 1)
    for i in range(len(y_o)):
        y.append(labeltranform[label.index(y_o[i])])
    y = np.array(y)
    print Counter(y)

    '''Data normalization'''
    scaler = StandardScaler().fit(data)
    X = scaler.transform(data)
    m, n = X.shape
    '''Discretization'''
    X_pd = pd.DataFrame(X, columns=['f' + str(i) for i in range(n)])
    k = 5
    X_bins = np.array([pd.cut(X_pd.iloc[:, i], k, labels=range(k)).values for i in range(n)])
    X_dis = pd.DataFrame(X_bins.T, columns=['f' + str(i) for i in range(n)])

    '''MRMR pre-rank the features'''
    X_fea = np.array(X_dis)

    num_fea = n

    idx = MRMR.mrmr(X_fea, y, n_selected_features=44)
    print idx[0]
    X_re = X_fea[:, idx[0]]

    '''Feature selection'''
    topk, index = LCC(X_re, y,miu=0.0804789,sigma=0.3177188)
    indexset = [int(i) for i in index]

    print len(indexset)
    subset = idx[:-topk]
    print subset

    '''Classification and performance evaluation.'''
    kf = KFold(n_splits=5,shuffle=True)
    clf = tree.DecisionTreeClassifier()
    acc = []
    X_dis = np.array(X_dis)
    X_update = X_dis[indexset]
    y_update = y[indexset]

    for (tr,te) in kf.split(X_update):
        X_tr = X_update[tr]
        y_tr = y_update[tr]
        clf.fit(X_tr[:, :], y_tr)
        X_te = X_update[te]
        y_te = y_update[te]
        predict = clf.predict(X_te[:, :])
        acc_score = accuracy_score(predict, y_te)
        acc.append(acc_score)
    print np.average(acc)
