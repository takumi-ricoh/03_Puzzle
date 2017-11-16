# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:15:56 2017

@author: p000495138
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edge = cv2.Canny(gray,20,20)

    # Display the resulting frame
    cv2.imshow('frame',edge)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()