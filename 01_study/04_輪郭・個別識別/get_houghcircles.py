# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 20:34:49 2017

@author: p000495138
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as random

#%% ラベリング1
img01 = cv2.imread("source.jpg")

img02 = cv2.cvtColor(img01,cv2.COLOR_BGR2GRAY)
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


plt.imshow(img07)