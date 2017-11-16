# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 20:11:22 2017

@author: waida
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
centroid = []

while(True):
    # Capture frame-by-frame
    ret, img1 = cap.read()

    # Our operations on the frame come here
    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    ret,img3 = cv2.threshold(img2,127,255,cv2.THRESH_BINARY)

    nlabels, labelimg, contours, CoGs = cv2.connectedComponentsWithStats(img3)
    curpos = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) + 1
    if nlabels > 0:
        for nlabel in range(1,nlabels): 
            x,y,w,h,size = contours[nlabel]
            xg,yg = CoGs[nlabel]

            # 面積フィルタ
            if size >= 100 and size <= 1000:
                centroid.append([xg, yg, size, curpos])
    print(centroid)



    # Display the resulting frame
    cv2.imshow('frame',img3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()