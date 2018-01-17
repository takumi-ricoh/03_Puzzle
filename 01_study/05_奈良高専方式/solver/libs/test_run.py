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

#プロット色々ためすための、、、
IMGN1 = 4 #サブプロット縦　個数
IMGN2 = 6 #サブプロット横　個数
plt.close("all")

#ファイルリスト取得
filelist = glob.glob("../../source_pic2/*.bmp") 
filelist.sort()


#画像読み出し
img_list = []
for idx,filepass in enumerate(filelist):
    img = cv2.imread(filepass)
    img_list.append(img)


#全ピース/エッジ/形状種類の情報取得(白ブロブ)
pieceinfo_list = []
for idx,img in enumerate(img_list):
    p = piece.Piece(img)
    p.get_pieceinfo()
    pieceinfo_list.append(p)        
    
#ソルバー （違う輪郭同士の比較に対応で　引数2つ)
solve  = solver.PuzzleSolver(pieceinfo_list, pieceinfo_list)
solved = solve.match_res_p

"""""""""""""""""""""""""""

### 以下評価用のプロット ###

"""""""""""""""""""""""""""

"""
#%% プロット1 : 輪郭/形状種類の確認

plt.figure(1)
for idx in range(len(pieceinfo_list)):
    #各ピース
    p = pieceinfo_list[idx]
    #サブプロット
    i = idx//4 + ((idx+4)%4)*6 + 1    
    plt.subplot(IMGN1,IMGN2,i)
    #元の画像
    plt.imshow(p.binary_img)
    #plt.imshow(p.img) 
    #輪郭
    plt.plot(p.contour_np[:,0],p.contour_np[:,1],"g")
    #スプライン後全輪郭
    plt.plot(p.contour_sp[:,0],p.contour_sp[:,1],"m")
    #各辺のスプライン後輪郭
    plt.plot(p.edges.curves_sp[0][:,0], p.edges.curves_sp[0][:,1], "r")
    plt.plot(p.edges.curves_sp[1][:,0], p.edges.curves_sp[1][:,1], "r")
    plt.plot(p.edges.curves_sp[2][:,0], p.edges.curves_sp[2][:,1], "r")
    plt.plot(p.edges.curves_sp[3][:,0], p.edges.curves_sp[3][:,1], "r")    
    #4つ角
    plt.plot(p.corner[:,0],p.corner[:,1],"r*")
    #軸を非表示
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")
    #形状タイプ
    #plt.title(p.shapetype.shapetype)

    #抜ける
    if idx == IMGN1*IMGN2 - 1:
        break
    
#%% プロット2 : 辺の長さの比較

#結果表示
plt.figure(2)
for idx in range(len(pieceinfo_list)):
    
    p=pieceinfo_list[idx]
    #print(idx)
    #サブプロット
    i = idx//4 + ((idx+4)%4)*6 + 1
    plt.subplot(IMGN1,IMGN2,i)
    
    #元の画像
    plt.imshow(p.binary_img)    

    #辺の長さ
    size=int(p.img_size[0]/2)
    #マゼンタ：曲線
    plt.text(15,size,           int(p.edges.lens_curve[1]),color="m",size=9) #left
    plt.text(size-10,15,        int(p.edges.lens_curve[0]),color="m",size=9) #up
    plt.text(size*2-30,size,    int(p.edges.lens_curve[3]),color="m",size=9) #right
    plt.text(size-10,size*2-20, int(p.edges.lens_curve[2]),color="m",size=9) #down
    #青：直線
    plt.text(15,size+100,           int(p.edges.lens_straight[1]),color="b",size=9) #left
    plt.text(size-10,15+100,        int(p.edges.lens_straight[0]),color="b",size=9) #up
    plt.text(size*2-30,size+100,    int(p.edges.lens_straight[3]),color="b",size=9) #right
    plt.text(size-10,size*2-20+100, int(p.edges.lens_straight[2]),color="b",size=9) #down
    #赤：合計
    plt.text(15,size+200,           int(p.edges.lens_total[1]),color="r",size=9) #left
    plt.text(size-10,15+200,        int(p.edges.lens_total[0]),color="r",size=9) #up
    plt.text(size*2-30,size+200,    int(p.edges.lens_total[3]),color="r",size=9) #right
    plt.text(size-10,size*2-20+200, int(p.edges.lens_total[2]),color="r",size=9) #down

    #軸を非表示
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")

    #抜ける
    if idx == IMGN1*IMGN2 - 1:
        break

#%% プロット3 : マッチング時のスコア表示(どこか1辺基準)

data = solve.all_scores[2]

#結果表示
plt.figure(3)
for idx in range(len(pieceinfo_list)):
    
    p=pieceinfo_list[idx]
    
    #サブプロット
    i = idx//4 + ((idx+4)%4)*6 + 1
    plt.subplot(IMGN1,IMGN2,i)
    #元の画像
    plt.imshow(p.binary_img)

    #スコア
    size=int(p.img_size[0]/2)
    score0 = data[idx*4+0,5]
    score1 = data[idx*4+1,5]
    score2 = data[idx*4+2,5]
    score3 = data[idx*4+3,5]
    plt.text(15,size,           np.round(score1, 3), color="m", size=9) #left
    plt.text(size-10,15,        np.round(score0, 3), color="m", size=9) #up
    plt.text(size*2-30,size,    np.round(score3, 3), color="m", size=9) #right
    plt.text(size-10,size*2-20, np.round(score2, 3), color="m", size=9) #down

    #軸を非表示
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")

    #抜ける
    if idx == IMGN1*IMGN2 - 1:
        break
"""
#%% プロット4 : 最適な位置

plt.figure(4)

for idx in range(len(pieceinfo_list)):

    p=pieceinfo_list[idx]
    
    #インデックス　→　位置　の辞書
    w0=solved[idx][0]
    w1=solved[idx][1]
    w2=solved[idx][2]
    w3=solved[idx][3]
    v2k = {0:"up",1:"left",2:"down",3:"right"}
    ww0 = str(w0[2]) + " - " + str(v2k[w0[3]])    
    ww1 = str(w1[2]) + " - " + str(v2k[w1[3]])     
    ww2 = str(w2[2]) + " - " + str(v2k[w2[3]])           
    ww3 = str(w3[2]) + " - " + str(v2k[w3[3]])         
    
    #サブプロット
    i = idx//4 + ((idx+4)%4)*6 + 1
    plt.subplot(IMGN1,IMGN2,i)
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

    #軸を非表示
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")
    
    
"""
#%% プロット5 : 形状認識

#結果表示
plt.figure(5)
for idx in range(len(pieceinfo_list)):
    
    p=pieceinfo_list[idx]
    #print(idx)
    #サブプロット
    i = idx//4 + ((idx+4)%4)*6 + 1
    plt.subplot(IMGN1,IMGN2,i)
    
    #元の画像
    plt.imshow(p.binary_img)    

    #辺の長さ
    size=int(p.img_size[0]/2)
    #マゼンタ：曲線
    plt.text(15,size,           p.shapetype.unevens[1],color="m",size=9) #left
    plt.text(size-10,15,        p.shapetype.unevens[0],color="m",size=9) #up
    plt.text(size*2-30,size,    p.shapetype.unevens[3],color="m",size=9) #right
    plt.text(size-10,size*2-20, p.shapetype.unevens[2],color="m",size=9) #down
"""    