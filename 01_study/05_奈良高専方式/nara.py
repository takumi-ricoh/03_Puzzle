# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 19:10:58 2017

@author: p000495138
"""

import cv2 #opencv
import numpy as np #ベクトル計算
import matplotlib.pyplot as plt #グラフ
import pandas as pd #データフレーム

#%%輪郭画像から隣接画素間の角度を計算
def contour2deg(contour):
    #最初と最後の画素のつなぎを計算するため、一旦最後の画素を頭につなげる
    contour = np.vstack([contour[-1,:],contour])
    #画素間の差分を計算
    diff = np.diff(contour,axis=0)    
    #画素間の角度計算
    atan = np.rad2deg(np.arctan2(diff[:,1],diff[:,0]))
    # -180°～180° → 0°～360°
    atan[atan<0] = atan[atan<0] + 360
    return np.int16(atan)

#%%Freeman chan code による、局所方向符号
def deg2cn(deg):
    cn = deg//45
    return cn

#%%局所曲率符号

#8の剰余の計算
def octmod(x):
    y = x%8
    return y

#局所曲率符号の計算
def cn2ca(cn):
    #最初と最後の画像のつなぎを計算するため、一旦最後の画素を頭につなげる
    cn = np.r_[cn[-1],cn]
    #cnの計算
    tmp=[]
    for idx,i in enumerate(cn): #enumerateは、インデックスと要素を同時に取り出せる
        if idx>0:#1つ目(最初と最後の画素のつなぎ目)を飛ばす
            tmp.append(octmod(cn[idx] -cn[idx-1] +11)-3) #論文記載の式
    tmp = np.array(tmp)
    return tmp

#%%Ｇオペレーション
def g_operation(ca,M): #何個平均化するか(M)を引数
    G=[]
    
    #M個の画素の平均を計算する際に、最初と最後の画像のつなぎが問題になる。
    #一旦前後に十分多い数add個だけ、要素をつなげておき、上記問題を回避する。
    add = 100 #平均化個数Mに対して、十分多い数を設定する。
    ca2 = np.r_[ca[-add:],ca,ca[:add]]
    
    for idx,i in enumerate(ca):
        idx = idx + add
        gsum = 0        
        #以下論文のG-operationの式
        for k in range(M-1):
            ca_minus = ca2[idx - k]
            ca_plus  = ca2[idx + k]
            gsum = gsum + (M-k)*(ca_minus + ca_plus)
        G.append(M*ca2[idx] + gsum)
    return np.array(G)

"""
以下実行部分
"""
#%%画像を読んで2値化
img1  = cv2.imread("01.bmp")
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret,img3 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY) 

#%%輪郭画素抽出
_, contours, hierarchy = cv2.findContours(img3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
contour = contours[0][:,0,:]

#%%局所方向符号
deg = contour2deg(contour)
cn = deg2cn(deg)

#%%局所曲率符号
ca = cn2ca(cn)

#%%Gオペレーション
g = g_operation(ca,M=10)
g_abs = np.abs(g) #Gは絶対値だと思うので絶対値に直す。

#%%計算したデータをdataframe形式のテーブルまとめる(pandasを使用)
g_table = np.c_[deg,cn,ca,contour,g_abs]
g_table = pd.DataFrame(g_table,columns=["deg","cn","ca","X","Y","G"])

#%%Gが大きいもの4点をピックアップする。
#やり方はいろいろあるが、一旦Gでソートしてから4個抽出
g_table2 = g_table.sort_values(by=["G"],ascending=False)
g_table2 = g_table2[:4]

#%%描画1(計算過程：データフレームのplot機能を利用)
"""
fig1 = plt.figure(1)

#fig1
ax1 = fig1.add_subplot(221)
g_table.plot.line(x="X",y="Y",style="-o",ax=ax1)
plt.grid(True)
plt.title("coordinate")
for k, v in g_table.iterrows():
    comment = str(v["X"])+"/"+str(v["Y"])
    ax1.annotate(comment,xy=(v["X"],v["Y"]),size=7)

#fig2
ax2 = fig1.add_subplot(222)
g_table.plot.line(x="X",y="Y",style="-o",ax=ax2)
plt.grid(True)
plt.title("deg")
for k, v in g_table.iterrows():
    ax2.annotate(v["deg"],xy=(v["X"],v["Y"]),size=7)

#fig3
ax3 = fig1.add_subplot(223)
g_table.plot.line(x="X",y="Y",style="-o",ax=ax3)
plt.grid(True)
plt.title("cn")
for k, v in g_table.iterrows():
    ax3.annotate(v["cn"],xy=(v["X"],v["Y"]),size=7)

#fig4
ax4 = fig1.add_subplot(224)
g_table.plot.line(x="X",y="Y",style="-o",ax=ax4)
plt.grid(True)
plt.title("ca")
for k, v in g_table.iterrows():
    ax4.annotate(v["ca"],xy=(v["X"],v["Y"]),size=7)

plt.tight_layout()

"""
#%%描画2(Gオペレーション結果：matplotlibで描画)
fig2 = plt.figure(2)
ax = fig2.add_subplot()
plt.scatter(g_table["X"],g_table["Y"],c=g_table["G"],cmap="gray",alpha=1)
plt.scatter(g_table2["X"],g_table2["Y"],marker="+",c="red",s=200)

plt.grid(True) #グラフへのグリッド追加
plt.title("G") #グラフへのタイトル追加
plt.tight_layout() #グラフのレイアウト調整
