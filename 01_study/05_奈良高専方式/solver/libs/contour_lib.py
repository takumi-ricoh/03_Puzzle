# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 16:17:43 2017

@author: p000495138
"""

import numpy as np
import cv2
from scipy import interpolate

#%% 2値化
def get_binaryimg(img):
    """
    Parameters
    ----------
    img : 画像
    
    Returns
    -------
    binary_img　: 2値化画像
    """    
    #画像を読んで2値化
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,img3 = cv2.threshold(img2, 120, 255, cv2.THRESH_BINARY)
    
    return img3



#%% 輪郭取得
def detect_contour(binary_img):
    """
    Parameters
    ----------
    binary_img : 2値化画像
    
    Returns
    -------
    contour_np　: 輪郭のnumpy配列[x,y]
    """

    #輪郭画素抽出
    _, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    contour = contours[0][:,0,:]
    
    #numpy 配列
    contour_np = np.array(contour)
    
    return contour_np



#%% 4箇所の角取得
def detect_4corner(contour_np, img_size=(0,0),margin=20):
    """
    Parameters
    ----------
    contour_np　: 輪郭のnumpy配列[x,y]
    img_size   ：　画像サイズのタプル(x,y)
    margin　　　　： 誤検知よけのマージン
    
    Returns
    -------
    corner_idx　：　4つ角のインデックスのリスト
    
    Notes
    -------
    輪郭座標の画像の4隅までの距離を計算する。
    近いものを角と認識させる。ただし画像の中央部を誤検出除けする。
    """
    
    con = contour_np  
    
    #画像サイズ
    xlen = img_size[0]
    ylen = img_size[1]

    #画像の4隅までの距離を計算
    f_dist = np.linalg.norm #距離計算
    len1 = f_dist(con - [0,0]        ,axis=1)
    len2 = f_dist(con - [xlen,0]     ,axis=1)
    len3 = f_dist(con - [0,ylen]     ,axis=1)
    len4 = f_dist(con - [xlen,ylen]  ,axis=1)
    
    #中央付近の座標を消す
    #まずブール計算してから除去する
    xcen = np.int32(xlen/2)
    ycen = np.int32(ylen/2)
    x_bool = ((xcen - margin)>con[:,0]) | ((xcen + margin)<con[:,0])
    y_bool = ((ycen - margin)>con[:,1]) | ((ycen + margin)<con[:,1])
    xy_bool = x_bool & y_bool

    #除去する距離は0にする
    len1 = len1*xy_bool
    len2 = len2*xy_bool
    len3 = len3*xy_bool
    len4 = len4*xy_bool
    
    #距離が最大となる4つのインデックスを抽出
    idx1 = np.argmax(len1)
    idx2 = np.argmax(len2)
    idx3 = np.argmax(len3)
    idx4 = np.argmax(len4)
    
    corner_idx = [idx1,idx2,idx3,idx4]
    
    #ソートする。重要!!!
    corner_idx.sort()
    
    return corner_idx


#%% 座標変換
def _calc_tf(data):
    """
    Parameters
    ----------
    data　: 座標変換前の曲線

    Returns
    -------
    res　：　始点～終点をx座標とした座標変換後データ
    
    Notes
    -------
    始点～終点までのベクトルを計算
    全データに対して座標変換を実施
    """    
    
    x=data[:,0]
    y=data[:,1]
    sx = np.array(x[0]) #始点
    sy = np.array(y[0])
    ex = np.array(x[-1]) #終点
    ey = np.array(y[-1])

    #始点～終点ベクトル
    u = np.array([ex-sx,ey-sy])
    #始点～曲線へのベクトル
    v = np.array([x - sx, y - sy]).T
    #ユークリッド距離計算
    f = np.linalg.norm 

    #uとvの角度(rad):  cosθ = 内積/|a||b]    
    theta = np.arccos(v@u/(f(u)*f(v,axis=1)))    
    #曲線から垂直に降ろした線の高さ
    height = np.cross(u, v) / f(u)
    #uベクトルに沿った新たな座標軸
    axis = f(v,axis=1)*np.cos(theta)
    axis[0]=0 #nan消す
    
    #マージ
    res = np.c_[axis,height]

    return res


#%% 輪郭を4つに切り出す
def split_contour(contour_np, corner_idx):
    """
    Parameters
    ----------
    contour_np　: 輪郭のnumpy配列[x,y]
    corner_idx　：　4つ角のインデックスのリスト

    Returns
    -------
    res　：　4辺の曲線のリスト(座標変換済み)
    
    Notes
    -------
    輪郭を切り出す。このとき元の輪郭の始点と終点をつなげる処理も行う。
    座標変換する。
    """       
        
    idx = corner_idx
    contour = contour_np
        
    #4つ角を基準にして、切り出す
    start    = contour[:idx[0]+1]
    end      = contour[idx[3]:]
    c1       = np.r_[end,start]
    c2       = contour[idx[0]:idx[1]+1]
    c3       = contour[idx[1]:idx[2]+1]
    c4       = contour[idx[2]:idx[3]+1]

    #座標変換する
    c1_tf    = _calc_tf(c1)
    c2_tf    = _calc_tf(c2)
    c3_tf    = _calc_tf(c3)
    c4_tf    = _calc_tf(c4)
    
    #リストに保存
    curves  = [c1_tf, c2_tf, c3_tf, c4_tf]

    return curves

#%%B-spline/Aperiodic
def calc_bspline(data,k=3,num=10):
    """
    Parameters
    ----------
    data　: 輪郭のnumpy配列[x,y]
    k　　　 ： スプライン近似の次数
    num　　:　スプライン実施回数  

    Returns
    -------
    res　：　スプライン実施後の値
    
    Notes
    -------
    輪郭を切り出す。このとき元の輪郭の始点と終点をつなげる処理も行う。
    座標変換する。
    """       
    
    x=data[:,0]
    y=data[:,1]
    
    for i in range(num):
        
        t = range(len(x))
        ipl_t = np.linspace(0.0, len(x) - 1, 100)
    
        x_tup = interpolate.splrep(t, x, k)
        y_tup = interpolate.splrep(t, y, k)
        
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
    
    res = np.c_[x_i,y_i]
    
    return res

#%%累積距離の計算
def curve_sum(data):
    """
    Parameters
    ----------
    data　: 輪郭のnumpy配列[x,y]

    Returns
    -------
    res　：　累積の配列
    
    Notes
    -------
    無し
    """       
    
    x = data[:,0]
    y = data[:,1]
    csum = np.cumsum(np.diff(x)**2 + np.diff(y)**2)
    csum = np.r_[0,csum]
    return csum
