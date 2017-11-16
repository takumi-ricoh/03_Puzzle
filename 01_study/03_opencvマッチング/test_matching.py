# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-

import cv2
import numpy as np

# 画像１
img1 = cv2.imread("Big.JPG")
# 画像２
img2 = cv2.imread("Small.JPG")

# A-KAZE検出器の生成
akaze = cv2.AKAZE_create()                                
surf = cv2.xfeatures2d.SURF_create()
sift = cv2.xfeatures2d.SIFT_create()

# 特徴量の検出と特徴量ベクトルの計算
kp1, des1 = akaze.detectAndCompute(img1, None)
kp2, des2 = akaze.detectAndCompute(img2, None)

kp3, des3 = surf.detectAndCompute(img1, None)
kp4, des4 = surf.detectAndCompute(img2, None)

kp5, des5 = sift.detectAndCompute(img1, None)
kp6, des6 = sift.detectAndCompute(img2, None)

#img2の画像にキーポイントを重ね書きする
#keyimage_akaze = cv2.drawKeypoints(img1,kp2,None)

# Brute-Force Matcher生成
bf = cv2.BFMatcher()

# 特徴量ベクトル同士をBrute-Force＆KNNでマッaaチング
matches1 = bf.knnMatch(des1, des2, k=2)
matches2 = bf.knnMatch(des3, des4, k=2)
matches3 = bf.knnMatch(des5, des6, k=2)
# データを間引きする
ratio1 = 0.7
ratio2 = 0.5
ratio3 = 0.4
good1 = []
good2 = []
good3 = []
best1 = 100
best2 = 100
best3 = 100
for m, n in matches1:
    if m.distance < ratio1 * n.distance:
        good1.append([m])
for m, n in matches2:
    if m.distance < ratio2 * n.distance:
        good2.append([m])
for m, n in matches3:
    if m.distance < ratio3 * n.distance:
        good2.append([m])
# 対応する特徴点同士を描画
nimg1 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good1, None, flags=2)
nimg2 = cv2.drawMatchesKnn(img1, kp3, img2, kp4, good2, None, flags=2)
nimg3 = cv2.drawMatchesKnn(img1, kp5, img2, kp6, good2, None, flags=2)
# 文字入力
nimg1 = cv2.putText(nimg1,"AKAZE",(50,50),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0))
nimg2 = cv2.putText(nimg2,"SURF",(50,50),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0))
nimg3 = cv2.putText(nimg3,"SIFT",(50,50),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0))

#仮の画像を作成
z = np.zeros_like(nimg3)

#画像をマージ
both1=np.hstack((nimg1,nimg2))
both2=np.hstack((nimg3,z))
both3 = np.vstack((both1,both2))
orgWidth, orgHeight = int(both3.shape[0]*2/3),int(both3.shape[1]*2/3)
both4=cv2.resize(both3,(orgHeight,orgWidth))
cv2.imshow('img', both4)

# キー押下で終了
cv2.waitKey(0)
cv2.destroyAllWindows()