# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:22:12 2017

@author: p000495138
"""
import copy
import cv2
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as random

#%% 元画像
img01 = cv2.imread("source.jpg")

#%% ﾓﾉｸﾛ化
img02 = cv2.cvtColor(img01,cv2.COLOR_BGR2GRAY)

#%% カラー次元
img03 = cv2.cvtColor(img02,cv2.COLOR_GRAY2BGR)

#%% 輪郭抽出
#引数1：画像、引数2：輪郭検索モード、引数3：輪郭近似方法
img04,contours,hierarchy = cv2.findContours(img02, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

rects=[]
for contour in contours:
    approx = cv2.convexHull(contour)
    rect = cv2.boundingRect(approx)
    rects.append(np.array(rect))

#%% ラベリング2
img06 = img01.copy()
#戻り。0:個数、1：labelImageと同じ、2：？、3：重心座標
label = cv2.connectedComponentsWithStats(bin)
# ラベルの個数
n=label[0]-1
# 重心位置
cog = np.delete(label[3],0,0)
# 重心に赤円を描く
for i in range(n):
    img06 = cv2.circle(img06,(int(cog[i][0]),int(cog[i][1])), 2, (0,0,255), -1)

#%%
plt.imshow(img06)

