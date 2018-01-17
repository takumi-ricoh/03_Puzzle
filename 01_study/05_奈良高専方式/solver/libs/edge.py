# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 00:29:03 2017

@author: takumi
"""

import numpy as np
from scipy import interpolate
import cv2

"""
################
各辺の情報
################
"""
class Edge():
    
    #スプライン補間パラメータ
    BSPLINE_POINTS = 1000 #補間後の点数
    
    def __init__(self,contour_np, corner_idx):
        self.contour_np = contour_np
        self.corner_idx = corner_idx

    #%% 辺情報の取得
    def get_edgeinfo(self):
        """
        Parameters
        ----------
        contour_np　: 輪郭のnumpy配列[x,y]
        corner_idx　：　4つ角のインデックスのリスト
    
        Returns
        -------
        curves      ：　切り出した4辺(リスト)
        curves_tf   ：　各4辺に座標変換を施したもの(リスト)
        curves_sp   ：　各4辺にスプライン処理を施したもの(リスト)
        curves_csum ：　各4辺の累積距離(リスト)
        straight_lens : 直線距離
        curve_lens   : 曲線距離
        curves_img   : エッジを画像化したもの
        
        """       
        
        #4辺の取得
        self.curves  = self._split_contour(self.contour_np, self.corner_idx)

        #スプライン処理の実施
        self.curves_sp    = []
        self.curves_tf    = []
        self.curves_csum  = []
        self.lens_straight = []
        self.lens_curve = []
        self.lens_total = []
        self.curves_img = []
        self.curves_img2 = []
        
        #1辺ごとに処理 →　リスト保存
        for curve in self.curves:
            self.curve_sp       = curve.copy()#self._bspline(curve, Edge.BSPLINE_K, Edge.BSPLINE_NUM, Edge.BSPLINE_POINTS)    #スプライン変換(配列)
            self.curve_sp       = self._bspline(curve, Edge.BSPLINE_POINTS)    #スプライン変換(配列)
            self.curve_tf       = self._tf(self.curve_sp)        #座標変換(配列)           
            self.curve_csum     = self._curve_sum(self.curve_tf) #累積長さ(配列)
            self.len_straight   = max(self.curve_tf[:,0])         #直線距離(スカラー)
            self.len_curve      = max(self.curve_csum)            #曲線距離(スカラー)
            self.len_total      = self.len_straight + self.len_curve
            self.curve_img      = self._toImg(self.curve_tf)
            self.curve_img2      = self._toImg2(self.curve_tf)
            
            self.curves_sp.append(self.curve_sp)
            self.curves_tf.append(self.curve_tf)
            self.curves_csum.append(self.curve_csum) 
            self.lens_straight.append(self.len_straight)
            self.lens_curve.append(self.len_curve)
            self.lens_total.append(self.len_total)
            self.curves_img.append(self.curve_img)
            self.curves_img2.append(self.curve_img2)
        
    #%% 輪郭を4つに切り出す
    def _split_contour(self,contour_np, corner_idx):
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
    
        #リストに保存
        curves  = [c1, c2, c3, c4]    
        
        return curves 
    
    #%% 座標変換
    def _tf(self,data):
        """        
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

        res = res[1:-1,:]
    
        return res

    #%%B-spline/Aperiodic
    def _bspline(self, data ,points):
        """
        Parameters
        ----------
        data　: 輪郭のnumpy配列[x,y]
        k　　　 ： スプライン近似の次数
        num　　:　スプライン実施回数  
    
        """       
        
        x=data[:,0]
        y=data[:,1]
                
        t = range(len(x))
        ipl_t = np.linspace(0.0, len(x) - 1, points)
    
        x_tup = interpolate.splrep(t, x, k=3, s=0)
        y_tup = interpolate.splrep(t, y, k=3, s=0)
        
        x_list = list(x_tup)
        xl = x.tolist()
        xl_addn = len(x_list) - len(xl)
        x_list[1] = xl + [0]*xl_addn
        
        y_list = list(y_tup)
        yl = y.tolist()
        yl_addn = len(y_list) - len(yl)
        y_list[1] = yl + [0]*yl_addn
        
        x_i = interpolate.splev(ipl_t, x_list)
        y_i = interpolate.splev(ipl_t, y_list)
    
        res = np.c_[x_i,y_i]
        
        return res

    #%%累積距離の計算
    def _curve_sum(self, data):
        """
        Returns
        -------
        res　：　累積距離の配列

        """       
        
        x = data[:,0]
        y = data[:,1]
        csum = np.sqrt(np.cumsum(np.diff(x)**2 + np.diff(y)**2))
        csum = np.r_[0,csum]
        return csum

    #%% Curve to Image
    def _toImg(self, data):
        """
        Parameters
        ----------
        data　: 輪郭のnumpy配列[x,y]    

        Returns
        -------
        res　：　累積距離の配列
        """       
        ctr = data.astype(np.int32)
        #位置調整
        ctr[:,0] = ctr[:,0] - min(ctr[:,0]) + 5
        ctr[:,1] = ctr[:,1] - min(ctr[:,1]) + 5
        
        #位置調整後のカーブ
        x=ctr[:,0]
        y=ctr[:,1]
        
        #ベース画像作成
        imgSize_x = np.uint32(max(x)-min(x) + 10)
        imgSize_y = np.uint32(max(y)-min(y) + 10)
        img = np.zeros((imgSize_y,imgSize_x),np.uint8)

        #コンターに記載
        img2 = cv2.drawContours(img.copy(),[ctr],-1,255,0 )
        return img2

    #%% Curve to Image
    def _toImg2(self, data):
        """
        Parameters
        ----------
        data　: 輪郭のnumpy配列[x,y]    

        Returns
        -------
        res　：　累積距離の配列
        """       
        ctr = data.astype(np.int32)
        #位置調整
        ctr[:,0] = ctr[:,0] - min(ctr[:,0]) + 10
        ctr[:,1] = ctr[:,1] - min(ctr[:,1]) + 10
        
        #位置調整後のカーブ
        x=ctr[:,0]
        y=ctr[:,1]
        
        #ベース画像作成
        imgSize_x = np.uint32(max(x)-min(x) + 20)
        imgSize_y = np.uint32(max(y)-min(y) + 20)
        img = np.zeros((imgSize_y,imgSize_x),np.uint8)

        img2 = img

        #コンターに記載
        for idx in range(len(ctr)):
            
            img2[int(ctr[idx,1]),int(ctr[idx,0])] = 255
            
        return img2
        