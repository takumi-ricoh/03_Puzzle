# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:18:36 2017

@author: p000495138
"""
import os
import cv2
import scipy.ndimage as nd
from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%%ファイルリスト
#現在 
thisdir = os.getcwd()
nextdir = os.chdir(thisdir + "./白色パズル")
print(os.getcwd())
files = os.listdir()

##%%データ読み出し
#リスト保存
datas = []

#データ整形(回転)
rot=[0,0,0,3,1,2,0,1,0,0,0,1,1,0,3,0,3,1,3,0,1,1,1,1]

for idx,i in enumerate(files):
    tmp = cv2.imread(i)
    tmp = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)
    ret,tmp = cv2.threshold(tmp,50,255,cv2.THRESH_BINARY)
    tmp = cv2.resize(tmp,(30,30))
    tmp = nd.rotate(tmp,rot[idx]*-90)
    datas.append(tmp)

#ベクトル化
datas2=[]
for i in datas:
    vec = i.reshape(900,)
    datas2.append(vec)
data_array = np.array(datas2)

#%%ラベル
#左から時計周りに
#凸-凹-凸-直：1
#凸-凹-凸-凹：2
#凹-凸-凹-直：3
#直-直-凹-凸：4
label = np.array([[0,1,1,2,0,2,1,1,1,2,1,1,0,3,3,0,3,2,0,2,3,0,1,2],])
#data_array = np.hstack([data_array,label.T])

#%%とりあえず、、
clf = SVC()
clf.fit(data_array,label.T)

#%%とりあえず試す
predict_result=clf.predict(data_array)

result = np.array([list(label[0]),list(predict_result)]).T
result = pd.DataFrame(result,columns=["answer","predict"])