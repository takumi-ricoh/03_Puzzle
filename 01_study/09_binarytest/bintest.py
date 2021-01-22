# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 21:11:16 2018

@author: p000495138
"""
import cv2 
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("C270image1001.bmp")

img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary_img = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY)

_, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE )
contour = contours[0][:,0,:]

#numpy 配列
contour_np = np.array(contour)

#img3 = img2 + binary_img*

plt.imshow(img)

plt.plot(contour_np[:,0],contour_np[:,1],"r",linewidth=1)