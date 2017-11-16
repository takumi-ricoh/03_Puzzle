# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 17:55:51 2017

@author: p000495138
"""

import cv2
import numpy as np
import 

cap.release()

#%%　重心取得関数
def get_center(img1,img2):
    
    #$ネガポジ逆転：ビット反転
    img3 = ~img2 
    
    #戻り。0:個数、1：labelImageと同じ、2：？、3：重心座標
    label = cv2.connectedComponentsWithStats(img3)
    
    # ラベルの個数
    n=label[0]-1

    # 重心位置
    cog = np.delete(label[3],0,0)

    # 重心に赤円を描く
    img4=img1.copy()
    for i in range(n):
        img4 = cv2.circle(img4,(int(cog[i][0]),int(cog[i][1])), 5, (0,0,255), -1)    
    
    return img4,cog

#%%　まとめ画像作成
def integration(img1,img2):
    dammy = np.zeros_like(img1)    
    both1=np.hstack((img1,img2))
    both2=np.hstack((dammy,dammy))
    both = np.vstack((both1,both2))
    return both


"""Capture video from camera"""
# カメラをキャプチャする
cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号

while True:
    # retは画像を取得成功フラグ
    ret, img01 = cap.read()

    # ﾓﾉｸﾛ化
    img02 = cv2.cvtColor(img01,cv2.COLOR_BGR2GRAY)

    #色のあるところを1、無いところを0
    ret, img03 = cv2.threshold(img02, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    #重心検知画像
    img04, cog = get_center(img01,img03)
    
    #円の検出
    circles = cv2.HoughCircles(img02,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))

    #%%統合画像
    img = integration(img01,img04)
    
    # フレームを表示する
    cv2.imshow('camera capture', img)

    k = cv2.waitKey(1) # 1msec待つ
    if k == 27: # ESCキーで終了
        break

# キャプチャを解放する
cap.release()
cv2.destroyAllWindows()
