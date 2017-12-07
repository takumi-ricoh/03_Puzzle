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

plt.close("all")
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

#%%B-spline/Aperiodic
def calc_bsplineA(curve):
    curve = curve.copy()
    x=curve["axis"]
    y=curve["height"]
    
    for i in range(10):
        
        t = range(len(x))
        ipl_t = np.linspace(0.0, len(x) - 1, 100)
    
        x_tup = interpolate.splrep(t, x, k=5)
        y_tup = interpolate.splrep(t, y, k=5)
        
        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]
        
        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]
        
        x_i = interpolate.splev(ipl_t, x_list)
        y_i = interpolate.splev(ipl_t, y_list)

        x=x_i
        y=y_i
    
    curve2 = pd.DataFrame([x_i,y_i]).T
    curve2.columns=["axis","height"]
    
    return curve2

#%%スプラインによる平滑化
def calc_smooth(curves):
    curves2=[]
    for curve in curves:
        curve2 = calc_bsplineA(curve)
        curves2.append(curve2)
        
    return curves2

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

#%%曲率の計算
def get_curvature(curves):
    curves = curves.copy()
    for curve in curves:
        x=curve["axis"]
        y=curve["height"]

        dx_dt = np.gradient(x)
        dy_dt = np.gradient(y)
        velocity = np.array([ [dx_dt[i], dy_dt[i]] for i in range(dx_dt.size)])    
        ds_dt = np.sqrt(dx_dt * dx_dt + dy_dt * dy_dt)    
        tangent = np.array([1/ds_dt] * 2).transpose() * velocity    
        tangent_x = tangent[:, 0]
        tangent_y = tangent[:, 1]    
        deriv_tangent_x = np.gradient(tangent_x)
        deriv_tangent_y = np.gradient(tangent_y)    
        dT_dt = np.array([ [deriv_tangent_x[i], deriv_tangent_y[i]] for i in range(deriv_tangent_x.size)])    
        length_dT_dt = np.sqrt(deriv_tangent_x * deriv_tangent_x + deriv_tangent_y * deriv_tangent_y)    
        normal = np.array([1/length_dT_dt] * 2).transpose() * dT_dt    
        d2s_dt2 = np.gradient(ds_dt)
        d2x_dt2 = np.gradient(dx_dt)
        d2y_dt2 = np.gradient(dy_dt)    
        curvature = np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt * dx_dt + dy_dt * dy_dt)**1.5
        t_component = np.array([d2s_dt2] * 2).transpose()
        n_component = np.array([curvature * ds_dt * ds_dt] * 2).transpose()
        
        acceleration = t_component * tangent + n_component * normal
 
        #変なのをはじく
        diff = np.r_[0,np.diff(curvature)]
        curvature[diff>0.1] = 0
    
        curve["curvature"]=curvature

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

#%%切り出した曲線から、画像への変換
def curves2img(curves):
    curveimgs = []
    for curve in curves:
        #輪郭を正の整数に直す
        data = np.array(curve[["axis","height"]])
        data[:,1] = data[:,1] - min(data[:,1]) + 5
        data = np.int32(data)
        #空の画像を生成
        xmax = int(max(data[:,0]))
        ymax = int(max(data[:,0]))
        img0 = np.ones([xmax,ymax])
        #輪郭を加えた画像を生成
        img1 = cv2.drawContours(img0,[data],-1,(0,255,0))
        curveimgs.append(img1)
        
    return curveimgs

#%%ファイル取得
filelist = glob.glob("./pic/*.bmp") 
filelist.sort()

#形状候補
shapelist = make_shapelist()

#画像を読んで、各種データをリスト保存
img_list = [] #画像を格納
contour_list = [] #輪郭と角の情報を格納
curve_list = [] #各4辺のデータに切り出した情報を格納
unevens_list = [] #4辺の凹凸データ
shaperesult_list = [] #形状タイプ確認結果
curveimgs_list = [] #各4辺のデータに切り出した画像を格納

for idx,i in enumerate(filelist):
    img = get_img(i)
    #輪郭取得
    contour = detect_corner(img)
    #4辺の曲線を取得
    curves = get_curve(contour)
    #平滑化
    curves = calc_smooth(curves)
    #累積長さの追加
    curves = curve_sum(curves)
    #曲率
    curves = get_curvature(curves)
    #画像生成
    curveimgs = curves2img(curves)    
    #凹凸情報を取得
    unevens = get_uneven(curves,img)
    #形状チェック
    shaperesult = check_shapetype(unevens,shapelist)
    
    #24個をまとめたリストに保存
    img_list.append(img) #画像
    contour_list.append(contour)#輪郭と角の情報
    curve_list.append(curves)#4つにｋ里出したもの
    curveimgs_list.append(curveimgs)
    unevens_list.append(unevens)
    shaperesult_list.append(shaperesult)
    

#%%パズルのマッチング
    
#scores=[]
#c1 = curve_list[0][0]
#e1 = curveimgs_list[0][0]
#
#for idxi,curve in enumerate(curve_list):
#    for idxj,c2 in enumerate(curves):
#        if unevens_list[idxi][idxj] == "bump":
#            d1 = np.array(c1[["axis","height"]])
#            d2 = np.array(c2[["axis","height"]])
#            d1[:,1] = d1[:,1] - min(d1[:,1]) + 5
#            d2[:,1] = d2[:,1] - min(d2[:,1]) + 5
#            d1 = np.int32(d1)
#            d2 = np.int32(d2)
#                        
#            e2 = curveimgs_list[idxi][idxj]
#            score = cv2.matchShapes(d1,d2,2,0.0)
#            #score = cv2.matchShapes(e1,e2,1,0.0)
#            #score=1
#            scores.append(score)

#%%グラフ表示
def plotter(c1,c2,score=0):
    x1,y1 = c1["axis"], c1["height"]
    x2,y2 = c2["axis"], c2["height"]    
    y1 =   y1 - y1.mean() #平均0
    y2 = (y2 - y2.mean() ) #平均0
    plt.plot(x1,y1,"-",linewidth=1)
    plt.plot(x2,y2,"-r",linewidth=1)
    plt.title("score="+str(score),size=8)
    plt.grid(True)
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")

def plotter2(c1,c2,score=0):
    x1,y1 = c1["csum"], c1["curvature"]
    x2,y2 = c2["csum"], c2["curvature"]    
    y1 =   y1 - y1.mean() #平均0
    y2 = (y2 - y2.mean() ) #平均0
    plt.plot(x1,y1,"-",linewidth=1)
    plt.plot(x2,y2,"-r",linewidth=1)
    plt.title("score="+str(score),size=8)
    plt.ylim([-0.1,0.1])
    plt.grid(True)
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")

#プロット1
plt.figure()
c1 = curve_list[0][0]
count = 1
for idx1,curves in enumerate(curve_list):
    for idx2,c2 in enumerate(curves):
        if unevens_list[idx1][idx2] == "hollow":
            plt.subplot(3,2,count)
            plotter(c1,c2)
            #plotter2(c1,c2,np.round(scores[count-1],5))
            if count == 5:
                break
            count = count+1
    else:
        continue
    break
plt.subplots_adjust(hspace=0.5)

#プロット1
plt.figure()
c1 = curve_list[0][0]
count = 1
for idx1,curves in enumerate(curve_list):
    for idx2,c2 in enumerate(curves):
        if unevens_list[idx1][idx2] == "hollow":
            plt.subplot(3,2,count)
            plotter2(c1,c2)
            #plotter2(c1,c2,np.round(scores[count-1],5))
            if count == 5:
                break
            count = count+1
    else:
        continue
    break
plt.subplots_adjust(hspace=0.5)


    
#%%グラフ表示
plt.figure()
for i in range(10):
    plt.subplot(3,4,i+1)
    plt.imshow(img_list[i])
    contour = contour_list[i]
    x = contour["X"]
    y = contour["Y"]
    plt.plot(x,y,c="blue")
    cx = x[contour.corner==1]
    cy = y[contour.corner==1]
    plt.scatter(cx,cy,marker="+",c="red",s=50)
    plt.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")
    #plt.title(str(i)+"/"+str(unevens_list[i]),size=9)
    plt.title("type="+str(shaperesult_list[i]),size=9)
