# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 18:13:06 2017

@author: p000495138
"""

import cv2 #opencv
import numpy as np #ベクトル計算
import matplotlib.pyplot as plt #グラフ
import pandas as pd #データフレーム
import glob
import itertools
from scipy import interpolate

plt.close(True)
#%%画像取得
def get_img(file):
    img  = cv2.imread(file)

    #画像を読んで2値化
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,img3 = cv2.threshold(img2, 120, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((1,1),np.uint8)
    img4 = cv2.morphologyEx(img3, cv2.MORPH_OPEN, kernel)
    
    return img4
    
#%%角検出
def detect_corner(binary_img):
    
    #輪郭画素抽出
    _, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    contour = contours[0][:,0,:]
    
    #データフレーム化
    contour_df = pd.DataFrame(contour.copy(),columns=["X","Y"]) 
        
    #距離の計算しデータフレームに追加
    len1 = np.linalg.norm(contour_df - [0,0] ,axis=1)
    len2 = np.linalg.norm(contour_df - [250,0] ,axis=1)
    len3 = np.linalg.norm(contour_df - [0,250]   ,axis=1)
    len4 = np.linalg.norm(contour_df - [250,250] ,axis=1)
    contour_df["len1"] = len1
    contour_df["len2"] = len2
    contour_df["len3"] = len3
    contour_df["len4"] = len4
    
    #中央付近の座標を消す
    a=((125-40)>contour_df["X"]) | ((125+40)<contour_df["X"]) #ブール
    b=((125-40)>contour_df["Y"]) | ((125+40)<contour_df["Y"]) #ブール
    contour_df2 = contour_df[a & b]
    
    #距離が最大となるインデックスを抽出
    ind1 = contour_df2.len1.idxmax()
    ind2 = contour_df2.len2.idxmax()
    ind3 = contour_df2.len3.idxmax()
    ind4 = contour_df2.len4.idxmax()
    
    #上記インデックスのデータを抽出
    contour_df["corner"] = np.zeros_like(len1)
    contour_df.loc[[ind1,ind2,ind3,ind4],"corner"] = 1
    #結果
    return contour_df

#%%座標変換したデータの計算
def get_tfdata(data):
    
    data = data.copy() #一旦コピー
    
    sx = np.array(data.iloc[0]["X"]) #始点
    sy = np.array(data.iloc[0]["Y"])
    ex = np.array(data.iloc[-1]["X"]) #終点
    ey = np.array(data.iloc[-1]["Y"])

    #始点～終点ベクトル
    u = np.array([ex-sx,ey-sy])
    #始点～曲線へのベクトル
    v = np.array([data["X"]-sx,data["Y"]-sy]).T

    #norm計算多いので名前つける
    f = np.linalg.norm

    #uとvの角度(rad):  cosθ = 内積/|a||b]    
    theta = np.arccos(v@u/(f(u)*f(v,axis=1)))    
    #曲線から垂直に降ろした線の高さ
    height = np.cross(u, v) / f(u)
    #uベクトルに沿った新たな座標軸
    axis = f(v,axis=1)*np.cos(theta)
    axis[0]=0 #nan消す
    #axisの、「元座標」 ：p1 + u/|u|*axis
    #x = sx + u[0]*(axis/f(u))
    #y = sy + u[1]*(axis/f(u))
    
    data["axis"] = axis
    data["height"]   = height

    return data
    
#%%角をつなぐ4辺に対する曲線抽出
def get_curve(contour):
    ###まず、cornerを4つに分割する
    
    #4点を基点にした順序の入れ替え
    idx = contour[contour.corner==1].index
    start  = contour[:idx[0]+1]
    d2     = contour[idx[0]:idx[1]+1]
    d3     = contour[idx[1]:idx[2]+1]
    d4     = contour[idx[2]:idx[3]+1]
    end    = contour[idx[3]:]
    d1     = end.append(start)
    
    #軸に沿って計算する
    curves=[]
    curves.append(get_tfdata(d1))
    curves.append(get_tfdata(d2))
    curves.append(get_tfdata(d3))
    curves.append(get_tfdata(d4))

    return curves

#%%凹凸情報の取得
def get_uneven(curves,img):
    unevens=[]
    for i in range(4):
        curve = curves[i] #pandas
        #heightの絶対値が最大となるときのheightをピックアップ
        curve["height_abs"] = np.abs(curve["height"])    #一旦絶対値の列を作る
        idxmax = curve.loc[curve["height_abs"].idxmax()] #インデックスを出す
        height = idxmax.loc["height"]
        #分類わけ
        if abs(height) < 10: #高さが5以下なら直線
            unevens.append("straight")
        elif height > 0:
            unevens.append("bump")
        else:
            unevens.append("hollow")
    return unevens

#%%チェックリスト生成
def make_shapelist():
    seq = ["straight","bump","hollow"]
    shapelist_all=[]
    shapelist=[]
    #全リストの生成
    for i in itertools.product(seq,repeat=4):
        shapelist_all.append(list(i))
    
    #回転して重複したものを除去
    for idx,i in enumerate(shapelist_all):
        for j in range(4):
            #並べ替えデータ
            tmp = i[:-1]
            tmp.insert(0,i[-1])
            #あるかのチェック
            if tmp in shapelist_all[:idx]:
                break
        else:
            shapelist.append(tmp)

    return shapelist

#%%形状タイプのチェック
def check_shapetype(unevens,shapelist):
    for idx,i in enumerate(shapelist):
        tmp = unevens.copy()
        for j in range(4):
            #候補の並べ替え
            tmp1 = tmp[:-1]
            tmp1.insert(0,tmp[-1])
            tmp = tmp1
            #チェック
            if tmp1 == i:
                print(tmp1)
                return idx
                break

#%%移動平均の計算
def mov_ave(x,num):
    b=np.ones(num)/num
    y=np.convolve(x, b, mode='same')#移動平均
    return y

#%%微分値の計算
def calc_diff(curves):
    curves = curves.copy()
    for curve in curves:
        x = curve.axis
        y = curve.height
        x_diff = np.r_[1,np.diff(x)]
        y_diff = np.r_[0,np.diff(y)]
        diff = y_diff/x_diff
        #移動平均
        diff2 = mov_ave(diff,5)
        curve["diff_curve"] = diff2
    
    return curves    

#%%グラフの移動平均
def curve2ave(curves):
    curves = curves.copy()
    for curve in curves:
        curve["height_ave"] = mov_ave(curve["height"],5)
        
    return curves    

#%%カーブに沿った累積距離
def curve_sum(curves):
    curves = curves.copy()
    for curve in curves:
        x = curve.axis
        y = curve.height
        csum = np.cumsum(np.diff(x)**2 + np.diff(y)**2)
        csum = np.r_[0,csum]
        curve["csum"] = csum
        
    return curves        

#%%ファイル取得
filelist = glob.glob("*.bmp") 
filelist.sort()

#形状候補
shapelist = make_shapelist()

#画像を読んで、各種データをリスト保存
img_list = [] #画像を格納
contour_list = [] #輪郭と角の情報を格納
curve_list = [] #各4辺のデータに切り出した情報を格納
unevens_list = [] #4辺の凹凸データ
shaperesult_list = [] #形状タイプ確認結果

for idx,i in enumerate(filelist):
    img = get_img(i)
    #輪郭取得
    contour = detect_corner(img)
    #4辺の曲線を取得
    curves = get_curve(contour)
    #4つの曲線を取得
    curves = curve2ave(curves)
    #1次微分の追加
    curves = calc_diff(curves)
    #累積長さの追加
    curves = curve_sum(curves)
    #凹凸情報を取得
    unevens = get_uneven(curves,img)
    #形状チェック
    shaperesult = check_shapetype(unevens,shapelist)
    
    #24個をまとめたリストに保存
    img_list.append(img) #画像
    contour_list.append(contour)#輪郭と角の情報
    curve_list.append(curves)#4つにｋ里出したもの
    unevens_list.append(unevens)
    shaperesult_list.append(shaperesult)

#%%パズルのマッチング
    
scores=[]
c1 = curve_list[8][1]

for idxi,curve in enumerate(curve_list):
    for idxj,c2 in enumerate(curves):
        if unevens_list[idxi][idxj] == "hollow":
            d1 = np.array(c1[["axis","height"]])
            d2 = np.array(c2[["axis","height"]])
            d1[:,1] = d1[:,1] - min(d1[:,1]) + 5
            d2[:,1] = d2[:,1] - min(d2[:,1]) + 5
            #score = cv2.matchShapes(d1,d2,3,0.0)
            score=1
            scores.append(score)

#%%グラフ表示
def plotter(c1,c2,score=0):
    
    x1,y1 = c1["axis"], c1["height_ave"]
    x2,y2 = c2["axis"], c2["height_ave"]    
    y1 =   y1 - y1.mean() #平均0
    y2 = -(y2 - y2.mean() ) #平均0
    plt.plot(x1,y1,"-",linewidth=1)
    plt.plot(x2,y2,"-r",linewidth=1)
    plt.title("score="+str(score),size=8)
    plt.grid(True)
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")
    
#プロット
c1 = curve_list[8][1]
count = 1
for idx1,curves in enumerate(curve_list):
    for idx2,c2 in enumerate(curves):
        if unevens_list[idx1][idx2] == "hollow":
            plt.subplot(3,3,count)
            plotter(c1,c2,np.round(scores[idx1],2))
            if count == 9:
                break
            count = count+1
    else:
        continue
    break
plt.subplots_adjust(hspace=0.5)
        
#%%グラフ表示
#plt.figure(2)
#for i in range(24):
#    plt.subplot(4,6,i+1)
#    plt.imshow(img_list[i])
#    contour = contour_list[i]
#    x = contour["X"][contour.corner==1]
#    y = contour["Y"][contour.corner==1]
#    plt.scatter(x,y,marker="+",c="red",s=50)
#    #plt.title(str(i)+"/"+str(unevens_list[i]),size=9)
#    plt.title("type="+str(shaperesult_list[i]),size=9)
#plt.subplots_adjust(wspace=0.4, hspace=0.6)
