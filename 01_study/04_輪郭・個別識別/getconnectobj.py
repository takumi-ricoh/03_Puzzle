# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 20:27:44 2017

@author: p000495138
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as random

#%% ラベリング1
img01 = cv2.imread("source.jpg")
img02 = cv2.cvtColor(img01,cv2.COLOR_BGR2GRAY)
height, width, channels = img01.shape[:3]
img05 = img01.copy()
#色のあるところを1、無いところを0
ret, bin = cv2.threshold(img02, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#$ネガポジ逆転：ビット反転
bin = ~bin 
#連結画像の抽出(nLabels：画像数、labelImage：画素に画像順を割り付けたもの)
nLabels, labelImage = cv2.connectedComponents(bin)
#色をランダムに割付
colors = []
for i in range(1, nLabels + 1):
    colors.append(np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))
#
for y in range(0, height):
    for x in range(0, width):
        if labelImage[y, x] > 0:
            img05[y, x] = colors[labelImage[y, x]]
        else:
            img05[y, x] = [0, 0, 0]

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

plt.imshow(img05)