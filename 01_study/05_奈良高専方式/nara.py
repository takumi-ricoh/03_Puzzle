# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 19:10:58 2017

@author: p000495138
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%%輪郭画像から隣接画像の角度を計算
def calc_deg2(contour):
    #最初と最後の画像のつなぎを計算するため、一旦最後の画素を頭につなげる
    contour = np.vstack([contour[-1,:],contour])
    #画素間の差分を計算
    diff = np.diff(contour,axis=0)    
    #画素間の角度計算
    atan = np.rad2deg(np.arctan2(diff[:,0],diff[:,1]))
    return atan

#%%局所方向符号
def freeman(deg):
    cn = deg//(-45) + 4
    return cn

#%%局所曲率符号
def octmod(x):
    y = x%8
    return y

def calc_ca(cn):
    #最初と最後の画像のつなぎを計算するため、一旦最後の画素を頭につなげる
    cn = np.r_[cn[-1],cn]
    #cnの計算
    tmp=[]
    for idx,i in enumerate(cn):
        if idx>0:
            tmp.append(octmod(cn[idx] -cn[idx-1] +11)-3)
    tmp = np.array(tmp)
    return tmp

#%%Ｇオペレーション
def g_operation(ca,M):
    G=[]
    add = 100
    #最初と最後の画像のつなぎを計算するため、一旦前後に10個ずつ加える
    ca2 = np.r_[ca[-add:],ca,ca[:add]]
    for idx,i in enumerate(ca):
        idx = idx + add
        gsum = 0
        for k in range(M-1):
            ca_minus = ca2[idx - k]
            ca_plus  = ca2[idx + k]
            gsum = gsum + (M-k)*(ca_minus + ca_plus)
        G.append(gsum)
    return np.array(G)

#%%画像を読んで2値化
img1  = cv2.imread("01.bmp")
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret,img3 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY) 

#%%輪郭画素抽出
_, contours, hierarchy = cv2.findContours(img3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
contour = contours[0][:,0,:]

#%%局所方向符号
deg = calc_deg2(contour)
cn = freeman(deg)

#%%局所曲率符号
ca = calc_ca(cn)

#%%Gオペレーション
g = g_operation(ca,M=30)

#%%まとめる
g_table = np.c_[cn,ca,contour,g]
g_table = pd.DataFrame(g_table,columns=["ca","cn","X","Y","G"])

#%%描画
fig = plt.figure()
#fig1
ax1 = fig.add_subplot(221)
g_table.plot(x="X",y="Y",kind="scatter",c="cn",ax=ax1)
plt.grid(True)
plt.title("cn")
#fig2
ax1 = fig.add_subplot(222)
g_table.plot(x="X",y="Y",kind="scatter",c="ca",ax=ax1)
plt.grid(True)
plt.title("ca")
#fig3
ax1 = fig.add_subplot(223)
g_table.plot(x="X",y="Y",kind="scatter",c="G",ax=ax1)
plt.grid(True)
plt.title("G")

plt.tight_layout()
##データのインデックス
#for k, v in g_table.iterrows():
#    ax.annotate(k,xy=(v[2]+3,v[3]+3),size=5)

