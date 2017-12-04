# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 19:56:05 2017

@author: p000495138
"""

import itertools
import numpy as np

#%%チェックリスト生成
def make_shapelist2():
    seq = ["straight","bump","hollow"]
    shapelist_all=[]
    shapelist=[]
    #全リストの生成
    for i in itertools.product(seq,repeat=4):
        shapelist_all.append(list(i))
    
    #重複の削除
    for idx,i in enumerate(shapelist_all):
        for j in range(4):
            #並べ替えデータ
            tmp = i[:-1]
            tmp.insert(0,i[-1])
            #あるかのチェック
            if tmp in shapelist_all[:idx]:
                break
        else:
            shapelist.append(tmp)

    return shapelist

a=make_shapelist2()
#%%チェックリスト生成

