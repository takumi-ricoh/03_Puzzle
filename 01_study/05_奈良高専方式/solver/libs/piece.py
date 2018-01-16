# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 16:17:43 2017

@author: p000495138
"""

import numpy as np
from scipy import interpolate
import cv2
import edge
import shapetype
import importlib
importlib.reload(edge)
importlib.reload(edge)

"""
################
1ピースの事前処理
################
"""

class Piece():
    
    #スプライン補間パラメータ
    BSPLINE_K = 3
    
    def __init__(self,img):
        self.img = img[40:-40,130:-130]
        
        
    #%% ピース計算
    def get_pieceinfo(self):
        """
        Parameters
        ----------
        img　       : 画像
    
        Returns
        -------
        binary_img  ：　2値化した画像(numpy配列)
        size        ：　画像サイズ(リスト)
        contour_np  ：　輪郭(numpy配列)
        corner      ：　4箇所の角の座標(リスト)
        corner_idx  ：　4箇所の角のインデックス
        edges       : 各辺のオブジェクト
        
        """       

        #2値化データ
        self.binary_img0 = self._get_binaryimg(self.img)
        self.img_size = self.binary_img0.shape
        
        self.binary_img = self._calc_morphology(self.binary_img0)
        
        #輪郭データ
        self.contour_np = self._detect_contour(self.binary_img)

        #スプライン補間
        self.contour_sp = self._bspline(self.contour_np)
        
        #4箇所の角のデータ
        self.corner_idx, self.corner = self._detect_4corner(self.contour_sp, self.img_size, margin=20)

        #各辺の情報取得
        self.edges = edge.Edge(self.contour_sp, self.corner_idx)
        self.edges.get_edgeinfo()

        #形状種類の取得
        self.shapetype = shapetype.ShapeType(self.edges.curves_tf)
        self.shapetype.get_typeinfo()
        

    #%% 2値化
    def _get_binaryimg(self,img):
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
        _, binary_img = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY)

        return binary_img

    #%% モルフォロジー処理
    def _calc_morphology(self,img):
        """
        Parameters
        ----------
        img : モノクロ画像
        
        Returns
        -------
        morph_img　: 変換後画像
        """    
        #画像を読んで2値化
        kernel = np.ones((10,10),np.uint8)
        img2 = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel) 
        
        return img2

    #%% 輪郭取得
    def _detect_contour(self,binary_img):
        """
        Parameters
        ----------
        binary_img : 2値化画像
        
        Returns
        -------
        contour_np　: 輪郭のnumpy配列[x,y]
        """
    
        #輪郭画素抽出
        _, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
        contour = contours[0][:,0,:]
        #RETR_CCOMP
        #RETR_EXTERNAL
        #cv2.CHAIN_APPROX_SIMPLE
        #cv2.CHAIN_APPROX_NONE 
        #cv2.CHAIN_APPROX_TC89_L1
        #cv2.CHAIN_APPROX_TC89_KCOS
        
        #numpy 配列
        contour_np = np.array(contour)
    
        return contour_np

    #%%B-spline/Aperiodic
    def _bspline(self, data, k=3, num=5):
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
            ipl_t = np.linspace(0.0, len(x)-1, 1000)
        
            x_tup = interpolate.splrep(t, x, k=3, s=0)
            y_tup = interpolate.splrep(t, y, k=3, s=0)
            
            x_list = list(x_tup)
            xl = x.tolist()
            xl_addn = len(x_list) - len(xl)
            x_list[1] = xl + [0]*xl_addn
#            x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]
            
            y_list = list(y_tup)
            yl = y.tolist()
            yl_addn = len(y_list) - len(yl)
            y_list[1] = yl + [0]*yl_addn
#            y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]
            
            x_i = interpolate.splev(ipl_t, x_list)
            y_i = interpolate.splev(ipl_t, y_list)
    
            x=x_i
            y=y_i
        
        res = np.c_[x_i,y_i]
        
        return res

    #%% 4箇所の角取得
    def _detect_4corner(self,contour_np, img_size=(0,0),margin=20):
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
        xlen = img_size[1]
        ylen = img_size[0]
    
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
    
        #除去する部分に大きいい値を加える
        xy_bool2 = ~xy_bool * 300
        len1 = len1+xy_bool2
        len2 = len2+xy_bool2
        len3 = len3+xy_bool2
        len4 = len4+xy_bool2
        
        #距離が最小となる4つのインデックスを抽出
        idx1 = np.argmin(len1)
        idx2 = np.argmin(len2)
        idx3 = np.argmin(len3)
        idx4 = np.argmin(len4)
        
        corner_idx = [idx1,idx2,idx3,idx4]
        
        #ソートする。重要!!!
        corner_idx.sort()
        #print(corner_idx)

        #4角の座標
        corner = contour_np[corner_idx,:]
        
        return corner_idx, corner

#%% 黒ブロブの処理(白ブロブを継承してつかう)
"""
################
黒ブロブ用の処理(Pieceを継承してつかう)
################
"""
class Piece_black(Piece):

    #ここをオーバーライドする
    def _detect_contour(self,binary_img):
        """
        Parameters
        ----------
        binary_img : 2値化画像
        
        Returns
        -------
        contour_np　: 輪郭のnumpy配列[x,y]
        """

        #ネガポジ反転する
        binary_img_nega = 255 - binary_img
        
        #輪郭画素抽出
        _, contours, hierarchy = cv2.findContours(binary_img_nega, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE )
        contour = contours[1][:,0,:]
        #cv2.CHAIN_APPROX_SIMPLE
        #cv2.CHAIN_APPROX_NONE 
        #cv2.CHAIN_APPROX_TC89_L1
        #cv2.CHAIN_APPROX_TC89_KCOS
        
        #numpy 配列
        contour_np = np.array(contour)
    
        return contour_np


