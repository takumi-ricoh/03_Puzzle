# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 00:29:03 2017

@author: takumi
"""

import numpy as np
from scipy import interpolate


"""
################
各辺の情報
################
"""
class Edge():
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
        
        """       
        
        #4辺の取得
        self.curves  = self._split_contour(self.contour_np, self.corner_idx)
        
        #座標変換
        self.curves_tf    = []
        for curve in self.curves:
            self.curves_tf.append(self._tf(curve))

#        #スプライン処理の実施
#        self.curves_sp    = []
#        for curve_tf in self.curves_tf:
#            self.curves_sp.append(self._bspline(curve_tf))

        #累積距離
        self.curves_csum    = []
        for curve in self.curves:
            self.curves_csum.append(self._curve_sum(curve))
            
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
    
        return res

    #%%B-spline/Aperiodic
    def _bspline(self, data, k=3, num=1):
        """
        Parameters
        ----------
        data　: 輪郭のnumpy配列[x,y]
        k　　　 ： スプライン近似の次数
        num　　:　スプライン実施回数  
    
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
    def _curve_sum(self, data):
        """
        Returns
        -------
        res　：　累積の配列

        """       
        
        x = data[:,0]
        y = data[:,1]
        csum = np.cumsum(np.diff(x)**2 + np.diff(y)**2)
        csum = np.r_[0,csum]
        return csum