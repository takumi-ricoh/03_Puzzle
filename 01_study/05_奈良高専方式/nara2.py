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

def calc_corner(img):
    #%%画像を読んで2値化
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,img3 = cv2.threshold(img2, 120, 255, cv2.THRESH_BINARY)
    
    #%%モルフォロジー変換？によるノイズ除去
    kernel = np.ones((1,1),np.uint8)
    img4 = cv2.morphologyEx(img3, cv2.MORPH_OPEN, kernel)
    
    #%%輪郭画素抽出
    _, contours, hierarchy = cv2.findContours(img4, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    contour = contours[0][:,0,:]
    
    #%%全く異なる方法
    #画像4点から最も近い4箇所をピックアップする
    contour2 = contour.copy() #輪郭座標
    
    #距離の計算
    len1 = np.linalg.norm(contour2 - [0,0] ,axis=1)
    len2 = np.linalg.norm(contour2 - [250,0] ,axis=1)
    len3 = np.linalg.norm(contour2 - [0,250]   ,axis=1)
    len4 = np.linalg.norm(contour2 - [250,250] ,axis=1)
    
    #中央付近の座標を除去
    a=((125-40)>contour2[:,0]) | ((125+40)<contour2[:,0])
    b=((125-40)>contour2[:,1]) | ((125+40)<contour2[:,1])
    len1 = len1[a & b]
    len2 = len2[a & b]
    len3 = len3[a & b]
    len4 = len4[a & b]
    contour3 = contour2[a & b]
    
    #距離が最大となるインデックスを抽出
    lenind1=np.argmax(len1)
    lenind2=np.argmax(len2)
    lenind3=np.argmax(len3)
    lenind4=np.argmax(len4)
    
    #上記インデックスのデータを抽出
    contour3=contour3[[lenind1,lenind2,lenind3,lenind4],:]

    return contour3

#%%実行部分
#ファイル取得
filelist = glob.glob("*.bmp") 
filelist.sort()

#画像を読んで、コーナーをリスト保存
img_list = []
corner_list = []
for idx,i in enumerate(filelist):
    img  = cv2.imread(i)
    corner = calc_corner(img)
    img_list.append(img)
    corner_list.append(corner)

#グラフ表示
for i in range(24):
    plt.subplot(6,4,i+1)
    plt.imshow(img_list[i])
    x = corner_list[i][:,0]
    y = corner_list[i][:,1]
    plt.scatter(x,y,marker="+",c="red",s=50)
plt.subplots_adjust(wspace=0, hspace=0.1)