# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 23:28:56 2017

@author: takumi
"""
import glob
import piece
import solver
import matplotlib.pyplot as plt
import numpy as np
import cv2

import importlib
importlib.reload(piece)
importlib.reload(solver)

plt.close()

#ファイルリスト取得
filelist = glob.glob("../../source_pic/*.bmp") 
filelist.sort()


#画像読み出し
img_list = []
for idx,filepass in enumerate(filelist):
    img = cv2.imread(filepass)
    img_list.append(img)


#全ピース/エッジ/形状種類の情報取得
pieceinfo_list = []
for img in img_list:
    p = piece.Piece(img)
    p.get_pieceinfo()
    pieceinfo_list.append(p)        


#ソルバー
solve  = solver.PuzzleSolver(pieceinfo_list)
#solved = solve.match_res_p

"""""""""""""""""""""""""""

### 以下評価用のプロット ###

"""""""""""""""""""""""""""


#%% プロット1 : 輪郭/形状種類の確認

plt.figure(1)
for idx in range(len(pieceinfo_list)):
    #各ピース
    p = pieceinfo_list(idx)
    #サブプロット
    plt.subplot(4,6,idx+1)
    #元の画像
    plt.imshow(p.img)
    #輪郭
    plt.plot(p.contour_np[:,0],p.contour_np[:,1],"g")
    #スプライン後全輪郭
    plt.plot(p.contour_sp[:,0],p.contour_sp[:,1])
    #各辺のスプライン後輪郭
    plt.plot(p.edges.curves_sp[0][:,0],p.edges.curves_sp[0][:,1],"y")
    plt.plot(p.edges.curves_sp[1][:,0],p.edges.curves_sp[1][:,1],"y")
    plt.plot(p.edges.curves_sp[2][:,0],p.edges.curves_sp[2][:,1],"y")
    plt.plot(p.edges.curves_sp[3][:,0],p.edges.curves_sp[3][:,1],"y")    
    #4つ角
    plt.plot(p.corner[:,0],p.corner[:,1],"r*")
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")
    #形状タイプ
    plt.title(p.shapetype.shapetype)
    


#%% プロット2 : 辺の長さの比較

#結果表示
plt.figure(2)
for idx in range(len(pieceinfo_list)):
    
    p=pieceinfo_list[idx]
    
    #サブプロット
    plt.subplot(4,6,idx+1)
    #元の画像
    plt.imshow(p.binary_img)    

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


#%% プロット3 : マッチング時のスコア表示(どこか1辺基準)

#リファレンスの1辺
ref = pieceinfo_list[1].edges.curves_img[3]

#結果表示
plt.figure(3)
for idx in range(len(pieceinfo_list)):
    
    p=pieceinfo_list[idx]
    
    #サブプロット
    plt.subplot(4,6,idx+1)
    #元の画像
    plt.imshow(p.binary_img)

    #スコア
    size=int(p.img_size[0]/2)
    score0=solved[idx][0][4]
    score1=solved[idx][1][4]
    score2=solved[idx][2][4]
    score3=solved[idx][3][4]
    plt.text(15,size,           np.round(score1, 3), color="m", size=9) #left
    plt.text(size-10,15,        np.round(score0, 3), color="m", size=9) #up
    plt.text(size*2-30,size,    np.round(score3, 3), color="m", size=9) #right
    plt.text(size-10,size*2-20, np.round(score2, 3), color="m", size=9) #down


#%% プロット4 : 最適な位置

plt.figure(4)

for idx in range(len(pieceinfo_list)):

    p=pieceinfo_list[idx]
    
    #インデックス　→　位置　の辞書
    w0=solved[idx][1][4]
    w1=solved[idx][1][4]
    w2=solved[idx][1][4]
    w3=solved[idx][1][4]
    v2k = {0:"up",1:"left",2:"down",3:"right"}
    ww0 = str(w0[2]) + " - " + str(v2k[w0[3]])    
    ww1 = str(w1[2]) + " - " + str(v2k[w1[3]])     
    ww2 = str(w2[2]) + " - " + str(v2k[w2[3]])             
    ww3 = str(w3[2]) + " - " + str(v2k[w3[3]])         
    
    #サブプロット
    plt.subplot(4,6,idx+1)
    #元の画像
    plt.imshow(p.binary_img)
    #ピース番号
    plt.title(idx)
    #テキスト
    size=int(p.img_size[0]/2)
    plt.text(15,size,           ww1,color="r",size=8) #left
    plt.text(size-10,15,        ww0,color="r",size=8) #up
    plt.text(size*2-30,size,    ww3,color="r",size=8) #right
    plt.text(size-10,size*2-20, ww2,color="r",size=8) #down        
