# encoding: utf-8
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from collections import Counter
from Con_method import ConsisCal
from sklearn.model_selection import KFold
from function.similarity_based import reliefF
from sklearn import tree
from sklearn.metrics import accuracy_score
from skfeature.function.information_theoretical_based import MRMR
from testwu2 import LCC
import time
from sko.GA import GA

if __name__ == "__main__":

    '''读取文件'''
    data = []
    y = []
    with open(r'D:\MyDocument\MyPaper\Rough set\Data\flow_wu.dat', 'r') as f:
        for line in f:
            if line != ' ':
                line = line.rstrip().split(',')
                data.append(line[:-1])
                y.append(line[-1])
            else:
                pass
    data = np.array(data, dtype=np.float)
    y_o = np.array(y, dtype=np.str_)

    '''将标签转化为数字'''
    y = []
    c = Counter(y_o)
    label = c.keys()
    category = len(label)
    labeltranform = range(1, len(label) + 1)
    for i in range(len(y_o)):
        y.append(labeltranform[label.index(y_o[i])])
    y = np.array(y)
    # print Counter(y)

    '''归一化'''
    scaler = StandardScaler().fit(data)
    X = scaler.transform(data)
    m, n = X.shape
    '''离散化'''
    X_pd = pd.DataFrame(X, columns=['f' + str(i) for i in range(n)])
    k = 5
    X_bins = np.array([pd.cut(X_pd.iloc[:, i], k, labels=range(k)).values for i in range(n)])
    X_dis = pd.DataFrame(X_bins.T, columns=['f' + str(i) for i in range(n)])

    '''reliefF 预排续'''
    X_fea = np.array(X_dis)
    # print X_fea.shape
    num_fea = n
    idx = MRMR.mrmr(X_fea, y, n_selected_features=44)
    print idx
    X_re = X_fea[:, idx]

    kf = KFold(n_splits=5, shuffle=True)
    clf = tree.DecisionTreeClassifier()

    def feature_selection(x):
        p = 0.8
        ipr = x[0]
        icr = x[1]

        global X_re
        global y
        '''特征选择'''
        topk, index = LCC(X_re, y=y, miu=icr, sigma=ipr)
        indexset = [int(i) for i in index]
        # print indexset
        S = len(indexset)
        global idx
        F = len(idx)
        subset = idx[:-topk]
        # print subset

        '''分类，进行特征测试'''
        global clf
        global kf
        acc = []
        X_dis = np.array(X_fea)
        X_dis = X_dis[:,subset]
        X_update = X_dis[indexset]
        y_update = y[indexset]

        D = 817

        for (tr, te) in kf.split(X_update):
            X_tr = X_update[tr]
            y_tr = y_update[tr]
            clf.fit(X_tr[:, :], y_tr)
            X_te = X_update[te]
            y_te = y_update[te]
            predict = clf.predict(X_te[:, :])
            acc_score = accuracy_score(predict, y_te)
            acc.append(acc_score)
        oa = np.average(acc)

        return (1-oa) * (1 - p) + (1-S / D + topk/F) * p/2



    start = time.time()
    print 'start>>>>'
    ga = GA(func=feature_selection,n_dim=2, max_iter=20, lb=[0, 0], ub=[0.3, 0.1])
    end = time.time()
    duration = end - start
    x_star, y_star = ga.fit()
    print('best_x:', x_star, 'best_y', y_star)
    Y_history = pd.DataFrame(ga.all_history_Y)
    print 'optimal history:',Y_history.index, '\n', Y_history.values
    print 'last time:',duration