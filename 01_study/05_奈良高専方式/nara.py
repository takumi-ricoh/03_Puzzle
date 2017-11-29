# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 19:10:58 2017

@author: p000495138
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def calc_deg2(contour):
    diff = np.diff(contour,axis=0)    
    atan = np.rad2deg(np.arctan2(diff[:,0],diff[:,1]))
    return atan

def freeman(deg):
    cn = deg//(-45) + 4
    return cn

def octmod(x):
    y = x%8
    return y

def calc_ca(cn):
    tmp=[]
    for idx,i in enumerate(cn):
        if idx>0:
            tmp.append(octmod(cn[idx] -cn[idx-1] +11)-3)
    tmp = np.array(tmp)
    return tmp

#画像を読んで2値化
img1  = cv2.imread("01.bmp")
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret,img3 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY) 

#輪郭画素抽出
_, contours, hierarchy = cv2.findContours(img3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
contour = contours[0][:,0,:]
plt.plot(contour[:,0],contour[:,1],".-")

#画素間の角度を計算
deg = calc_deg2(contour)

#局所方向符号
cn = freeman(deg)

#局所曲率符号
ca = calc_ca(cn)
