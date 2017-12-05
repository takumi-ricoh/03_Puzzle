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
from scipy import signal
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
    ex = np.array(data.iloc[-1]["X"]) #始点
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
    x = sx + u[0]*(axis/f(u))
    y = sy + u[1]*(axis/f(u))
    
    data["new_axis"] = axis
    data["height"]   = height

    return data
    
#%%角をつなぐ直線に対する曲線抽出
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

#%%相互相関関数のチェック
def calc_correlation(c1,c2):
    
    #等間隔(サンプリング)に直す
    t = np.linspace(0,int(max(c1.new_axis)),1001)
    x1,y1 = c1.new_axis, c1.height
    x2,y2 = c2.new_axis, c2.height    
    f1 = interpolate.interp1d(c1.new_axis, c1.height, kind="linear",bounds_error=False)
    f2 = interpolate.interp1d(c2.new_axis, c2.height, kind="linear",bounds_error=False)    
    h1=f1(t)
    h2=f2(t)
    #tck1 = interpolate.splrep(c1.new_axis, c1.height,s=0)
    #tck2 = interpolate.splrep(c2.new_axis, c2.height,s=0)   
    #h1 = interpolate.splev(x,tck1)
    #h2 = interpolate.splev(x,tck2)
#    f1 = interpolate.make_interp_spline(c1.new_axis, c1.height)
#    f2 = interpolate.make_interp_spline(c2.new_axis, c2.height)    
#    h1=f1(x)
#    h2=f2(x)    
    #h1 = f1(x) - f1(x).mean() #平均0
    #h2 = -( f2(x) - f2(x).mean() ) #平均0
    #相互相関
    corr = np.correlate(h1,h2,"full")
    
    return [h1,h2,corr]

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
    #4つの曲線を取得
    curves = get_curve(contour)
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
match=[]
c1 = curve_list[0][1]
c2 = curve_list[0][2]


#for idxi,i in enumerate(curve_list):
#    for idxj,j in enumerate(i):
#        if unevens_list[idxi][idxj] == "hollow":
#            res = calc_correlation(c1,j)
#            match.append(res)
        
#%%グラフ表示
for i in range(24):
    plt.subplot(4,6,i+1)
    plt.imshow(img_list[i])
    contour = contour_list[i]
    x = contour["X"][contour.corner==1]
    y = contour["Y"][contour.corner==1]
    plt.scatter(x,y,marker="+",c="red",s=50)
    #plt.title(str(i)+"/"+str(unevens_list[i]),size=9)
    plt.title("type="+str(shaperesult_list[i]),size=9)
plt.subplots_adjust(wspace=0.4, hspace=0.6)

#
#fig = plt.figure(2)
#for j in range(4):
#    ax = fig.add_subplot(2,2,j+1)
#    curve_list[0][j].plot(x="new_axis",y="height",ax=ax)
#    #curve_list[0][j].plot(x="onaxisx",y="onaxisy",ax=ax)

#plt.figure(2)
#plt.imshow(img_list[0])