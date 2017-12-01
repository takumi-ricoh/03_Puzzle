# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 18:13:06 2017

@author: p000495138
"""

import cv2 #opencv
import numpy as np #ベクトル計算
import matplotlib.pyplot as plt #グラフ
import pandas as pd #データフレーム
import glob
import itertools

#%%画像取得
def get_img(file):
    img  = cv2.imread(file)

    #画像を読んで2値化
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,img3 = cv2.threshold(img2, 120, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((1,1),np.uint8)
    img4 = cv2.morphologyEx(img3, cv2.MORPH_OPEN, kernel)
    
    return img4
    
#%%角検出
def detect_corner(binary_img):
    
    #輪郭画素抽出
    _, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    contour = contours[0][:,0,:]
    
    #データフレーム化
    contour_df = pd.DataFrame(contour.copy(),columns=["X","Y"]) 
        
    #距離の計算しデータフレームに追加
    len1 = np.linalg.norm(contour_df - [0,0] ,axis=1)
    len2 = np.linalg.norm(contour_df - [250,0] ,axis=1)
    len3 = np.linalg.norm(contour_df - [0,250]   ,axis=1)
    len4 = np.linalg.norm(contour_df - [250,250] ,axis=1)
    contour_df["len1"] = len1
    contour_df["len2"] = len2
    contour_df["len3"] = len3
    contour_df["len4"] = len4
    
    #中央付近の座標を消す
    a=((125-40)>contour_df["X"]) | ((125+40)<contour_df["X"]) #ブール
    b=((125-40)>contour_df["Y"]) | ((125+40)<contour_df["Y"]) #ブール
    contour_df2 = contour_df[a & b]
    
    #距離が最大となるインデックスを抽出
    ind1 = contour_df2.len1.idxmax()
    ind2 = contour_df2.len2.idxmax()
    ind3 = contour_df2.len3.idxmax()
    ind4 = contour_df2.len4.idxmax()
    
    #上記インデックスのデータを抽出
    contour_df["corner"] = np.zeros_like(len1)
    contour_df.loc[[ind1,ind2,ind3,ind4],"corner"] = 1
    #結果
    return contour_df

#%%座標変換したデータの計算
def get_tfdata(data):
    
    data = data.copy() #一旦コピー
    
    sx = np.array(data.iloc[0]["X"]) #始点
    sy = np.array(data.iloc[0]["Y"])
    ex = np.array(data.iloc[-1]["X"]) #始点
    ey = np.array(data.iloc[-1]["Y"])

    #始点～終点ベクトル
    u = np.array([ex-sx,ey-sy])
    #始点～曲線へのベクトル
    v = np.array([data["X"]-sx,data["Y"]-sy]).T

    #norm計算多いので名前つける
    f = np.linalg.norm

    #uとvの角度(rad):  cosθ = 内積/|a||b]    
    theta = np.arccos(v@u/(f(u)*f(v,axis=1)))    
    #曲線から垂直に降ろした線の高さ
    height = np.cross(u, v) / f(u)
    #uベクトルに沿った新たな座標軸
    axis = f(v,axis=1)*np.cos(theta)
    axis[0]=0 #nan消す
    #axisの、「元座標」 ：p1 + u/|u|*axis
    x = sx + u[0]*(axis/f(u))
    y = sy + u[1]*(axis/f(u))
    
    data["new_axis"] = axis
    data["height"]   = height
    data["onaxisx"] = np.int32(np.round(x))
    data["onaxisy"] = np.int32(np.round(y))

    return data
    
#%%角をつなぐ直線に対する曲線抽出
def get_curve(contour):
    ###まず、cornerを4つに分割する
    
    #4点を基点にした順序の入れ替え
    idx = contour[contour.corner==1].index
    start  = contour[:idx[0]+1]
    d2     = contour[idx[0]:idx[1]+1]
    d3     = contour[idx[1]:idx[2]+1]
    d4     = contour[idx[2]:idx[3]+1]
    end    = contour[idx[3]:]
    d1     = end.append(start)
    
    #軸に沿って計算する
    curves=[]
    curves.append(get_tfdata(d1))
    curves.append(get_tfdata(d2))
    curves.append(get_tfdata(d3))
    curves.append(get_tfdata(d4))

    return curves

#%%凹凸情報の取得
def get_uneven(curves,img):
    unevens=[]
    for i in range(4):
        curve = curves[i] #pandas
        #heightの絶対値が最大となる行をピックアップ
        curve["height_abs"] = np.abs(curve["height"]) 
        idxmax = curve.loc[curve["height_abs"].idxmax()]
        #この場合のonaxisが、黒か白かで判別
        x = int(idxmax["onaxisx"]) #なのでint二変換
        y = int(idxmax["onaxisy"]) #画素なのでint二変換
        height = idxmax.loc["height"]
        if abs(height) < 10: #高さが5以下なら直線
            unevens.append("straight")
#        elif img[x,y] > 100: #img位置が白なら 
#            unevens.append("bump")
#        else:
#            unevens.append("hollow")
        elif height > 0:
            unevens.append("bump")
        else:
            unevens.append("hollow")
    return unevens

#%%実行部分
#ファイル取得
filelist = glob.glob("*.bmp") 
filelist.sort()

#画像を読んで、各種データをリスト保存
img_list = [] #画像を格納
contour_list = [] #輪郭と角の情報を格納
curve_list = [] #4つに切り出した情報を格納
unevens_list = [] #4つに切り出した情報を格納
for idx,i in enumerate(filelist):
    #2値画像取得
    img = get_img(i)
    #輪郭取得
    contour = detect_corner(img)
    #4つの曲線を取得
    curves = get_curve(contour)
    #凹凸情報を取得
    unevens = get_uneven(curves,img)
    #形状チェック
    

    #24個をまとめたリストに保存
    img_list.append(img)
    contour_list.append(contour)
    curve_list.append(curves)
    unevens_list.append(unevens)

d = make_shapelist()

#グラフ表示
for i in range(24):
    plt.subplot(4,6,i+1)
    plt.imshow(img_list[i])
    contour = contour_list[i]
    x = contour["X"][contour.corner==1]
    y = contour["Y"][contour.corner==1]
    plt.scatter(x,y,marker="+",c="red",s=50)
    plt.title(str(i)+"/"+str(unevens_list[i]),size=9)
plt.subplots_adjust(wspace=0.4, hspace=0.6)

fig = plt.figure(2)
for j in range(4):
    ax = fig.add_subplot(2,2,j+1)
    curve_list[0][j].plot(x="new_axis",y="height",ax=ax)
    #curve_list[0][j].plot(x="onaxisx",y="onaxisy",ax=ax)

#plt.figure(2)
#plt.imshow(img_list[0])