# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 23:28:56 2017

@author: takumi
"""
import glob
import piece
import matplotlib.pyplot as plt
import cv2

import importlib
importlib.reload(piece)

#ファイルリスト取得
filelist = glob.glob("../../source_pic/*.bmp") 
filelist.sort()

#結果
for idx,i in enumerate(filelist):
    img = cv2.imread(i)
    p = piece.Piece(img)
    p.get_pieceinfo()

    #plot
    plt.figure(1)
    plt.subplot(4,6,idx+1)
    plt.imshow(p.img)
    plt.plot(p.corner[:,0],p.corner[:,1],"r*")
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")
    #形状タイプ
    plt.title(p.shapetype.shapetype)
    #辺の長さ
    plt.text(10,125,int(max(p.edges.curves_tf[0][:,0])),color="y")
    plt.text(110,40,int(max(p.edges.curves_tf[1][:,0])),color="y")
    plt.text(200,125,int(max(p.edges.curves_tf[2][:,0])),color="y")
    plt.text(110,240,int(max(p.edges.curves_tf[3][:,0])),color="y")
    