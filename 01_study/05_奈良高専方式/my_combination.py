# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 19:56:05 2017

@author: p000495138
"""

import itertools
import numpy as np
#%%形状リスト生成
def make_shapelist():
    stype = ["straight","bump","hollow"]
    shapelist = list(itertools.combinations_with_replacement(stype,4))
    return shapelist

a=make_shapelist()

b=[]
for i in a:
    tmp = np.random.permutation(list(i))
    #print(tmp)
    b.append(tmp)
