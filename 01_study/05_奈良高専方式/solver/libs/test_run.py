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

plt.close()

#ファイルリスト取得
filelist = glob.glob("../../source_pic/*.bmp") 
filelist.sort()

a=[]
#結果
for idx,filepass in enumerate(filelist):
    img = cv2.imread(filepass)
    p = piece.Piece(img,filepass)
    p.get_pieceinfo()

    #plot
    plt.figure(1)
    plt.subplot(4,6,idx+1)
    #元の画像
    plt.imshow(p.img)
    plt.plot(p.contour_np[:,0],p.contour_np[:,1])
    #スプライン後輪郭
    plt.plot(p.edges.curves_sp[0][:,0],p.edges.curves_sp[0][:,1],"y")
    plt.plot(p.edges.curves_sp[1][:,0],p.edges.curves_sp[1][:,1],"y")
    plt.plot(p.edges.curves_sp[2][:,0],p.edges.curves_sp[2][:,1],"y")
    plt.plot(p.edges.curves_sp[3][:,0],p.edges.curves_sp[3][:,1],"y")    
    #4つ角
    plt.plot(p.corner[:,0],p.corner[:,1],"r*")
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")
    #形状タイプ
    plt.title(p.shapetype.shapetype)
    
    #辺の長さ
    size=int(p.img_size[0]/2)
    plt.text(15,size,           int(p.edges.lens_curve[1]),color="m",size=9) #left
    plt.text(size-10,15,        int(p.edges.lens_curve[0]),color="m",size=9) #up
    plt.text(size*2-30,size,    int(p.edges.lens_curve[3]),color="m",size=9) #right
    plt.text(size-10,size*2-20, int(p.edges.lens_curve[2]),color="m",size=9) #down
    plt.text(15,size+10,           int(p.edges.lens_straight[1]),color="b",size=9) #left
    plt.text(size-10,15+10,        int(p.edges.lens_straight[0]),color="b",size=9) #up
    plt.text(size*2-30,size+10,    int(p.edges.lens_straight[3]),color="b",size=9) #right
    plt.text(size-10,size*2-20+10, int(p.edges.lens_straight[2]),color="b",size=9) #down
    plt.text(15,size+20,           int(p.edges.lens_total[1]),color="r",size=9) #left
    plt.text(size-10,15+20,        int(p.edges.lens_total[0]),color="r",size=9) #up
    plt.text(size*2-30,size+20,    int(p.edges.lens_total[3]),color="r",size=9) #right
    plt.text(size-10,size*2-20+20, int(p.edges.lens_total[2]),color="r",size=9) #down
    
    #plt.tight_layout()
    
    a.append(p.corner)
    
#    plt.figure(2)
#    plt.subplot(4,6,idx+1)
#    plt.imshow(p.binary_img)
#    
#    plt.figure(3)
#    plt.subplot(4,6,idx+1)
#    plt.imshow(p.morph_img)

    
#    if idx>7:
#        break