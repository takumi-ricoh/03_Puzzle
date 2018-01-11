# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 23:28:56 2017

@author: takumi
"""
import glob
import piece
import matplotlib.pyplot as plt
import numpy as np
import cv2

import importlib
importlib.reload(piece)

plt.close()

#ファイルリスト取得
filelist = glob.glob("../../source_pic/*.bmp") 
filelist.sort()

piecelist=[]
shapelist=[]
#結果
for idx,filepass in enumerate(filelist):
    img = cv2.imread(filepass)
    p = piece.Piece(img,filepass)
    p.get_pieceinfo()

    piecelist.append(p)   


    """
    プロット1 : 距離による比較
    """
    plt.figure(1)
    plt.subplot(4,6,idx+1)
    #元の画像
    plt.imshow(p.img)
    #輪郭
    plt.plot(p.contour_np[:,0],p.contour_np[:,1],"g")
    #スプライン後輪郭
    plt.plot(p.contour_sp[:,0],p.contour_sp[:,1])
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
    
    """
    プロット2 ：　matchShapesによる比較
    """

    if idx==1:
        ref = p.edges.curves_img[3]
#        plt.figure(3)
#        plt.subplot()
#        plt.imshow(ref,origin="lower")
#        print("refType=",p.shapetype.unevens[3])

    plt.figure(2)
    plt.subplot(4,6,idx+1)

    #値が小さいほど良い    
    s0=cv2.matchShapes(ref, p.edges.curves_img[0] ,3 ,0.0)
    s1=cv2.matchShapes(ref, p.edges.curves_img[1] ,3 ,0.0)
    s2=cv2.matchShapes(ref, p.edges.curves_img[2] ,3 ,0.0)
    s3=cv2.matchShapes(ref, p.edges.curves_img[3] ,3 ,0.0)    
        
    #元の画像
    plt.imshow(p.binary_img)

    #辺の長さ
    size=int(p.img_size[0]/2)
    plt.text(15,size,           np.round(s1,3),color="m",size=9) #left
    plt.text(size-10,15,        np.round(s0,3),color="m",size=9) #up
    plt.text(size*2-30,size,    np.round(s3,3),color="m",size=9) #right
    plt.text(size-10,size*2-20, np.round(s2,3),color="m",size=9) #down

#matchshapesによる比較
tmp=[]
scores=[]#比較したインデックスと、そのスコア
#基準の辺
for idx,i in enumerate(piecelist):
    for ii in range(4):
        #比較する辺
        for jdx,j in enumerate(piecelist):
            for jj in range(4):
                ref = i.edges.curves_img[ii]
                obj = j.edges.curves_img[jj]
                s = cv2.matchShapes(ref,obj,3,0.0)

                #形状の合致
                ref_shape = piecelist[idx].shapetype.unevens[ii]
                obj_shape = piecelist[jdx].shapetype.unevens[jj]
                if (ref_shape=="convex") and (obj_shape=="concave"):
                    flag=1
                elif (ref_shape=="concave") and (obj_shape=="convex"):
                    flag=1
                elif ref_shape=="straight":
                    flag=1
                else:
                    flag=0
        
                tmp.append([idx,ii,jdx,jj,s,flag])
        tmp=np.array(tmp)
        scores.append(tmp)
        tmp=[]

#ベストスコア抽出
bestscores=[]    
for kdx,k in enumerate(scores):
    #形状が該当するもののみ
    a=k
    b=a[a[:,5]==1]
    #コノ中でスコア最小となるインデックス    
    c=np.argmin(b[:,4])
    #該当行を抽出
    d=b[c,:]
    
    bestscores.append(d)

for ndx,n in enumerate(bestscores):
    #プロット
    #表示ワード
    plt.figure(4)
    #元の画像
    jo1 = ndx%4
    jo2 = int(ndx/4)
    if jo1==0:
        w0=np.int8(bestscores[ndx])
        w1=np.int8(bestscores[ndx+1])
        w2=np.int8(bestscores[ndx+2])
        w3=np.int8(bestscores[ndx+3])
        v2k = {0:"up",1:"left",2:"down",3:"right"}
        ww0 = str(w0[2]) + " - " + str(v2k[w0[3]])    
        ww1 = str(w1[2]) + " - " + str(v2k[w1[3]])     
        ww2 = str(w2[2]) + " - " + str(v2k[w2[3]])             
        ww3 = str(w3[2]) + " - " + str(v2k[w3[3]])     
        
        plt.subplot(4,6,jo2+1)
        p=piecelist[jo2]
        plt.imshow(p.img)
        plt.title(jo2)
        
        size=int(p.img_size[0]/2)
        plt.text(15,size,           ww1,color="r",size=8) #left
        plt.text(size-10,15,        ww0,color="r",size=8) #up
        plt.text(size*2-30,size,    ww3,color="r",size=8) #right
        plt.text(size-10,size*2-20, ww2,color="r",size=8) #down    
    
bestscores_np = np.array(bestscores)



    
#    plt.figure(2)
#    plt.subplot(4,6,idx+1)
#    plt.imshow(p.binary_img)
#    
#    plt.figure(3)
#    plt.subplot(4,6,idx+1)
#    plt.imshow(p.morph_img)

    
#    if idx>7:
#        break