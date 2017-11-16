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
img01 = cv2.imread("source2.jpg")

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

#%% ラベリング1
height, width, channels = img01.shape[:3]
img05 = copy.copy(img01)

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

#%% 円の検出（重い）
img07 = img01.copy()    
circles = cv2.HoughCircles(img02,cv2.HOUGH_GRADIENT,1,20,
                            param1=30,param2=30,minRadius=0,maxRadius=150)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img07,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    #cv2.circle(img01,(i[0],i[1]),2,(0,0,255),3)

    

#%%
cv2.imshow("aaa",img08)
cv2.waitKey(0)
cv2.destroyAllWindows()
