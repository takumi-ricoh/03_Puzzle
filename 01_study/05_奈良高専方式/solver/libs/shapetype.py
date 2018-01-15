#coding: utf-8 -*-
"""
Created on Wed Dec 27 18:07:47 2017

@author: p000495138
"""
import numpy as np
import itertools

"""
################
形状種類の情報
################
"""
class ShapeType():
    
    def __init__(self, curves_tf):
        self.curves_tf = curves_tf
    
    #%% 辺情報の取得
    def get_typeinfo(self):
        """
        Parameters
        ----------
        curves　: 4辺のリスト
    
        Returns
        -------
        candidate   ：　形状候補(リスト)
        unevens     ：　4辺の形状判定結果(リスト)
        shapetype   ：　形状種類の判定結果(整数)        
        """      
        #形状候補の取得
        self.candidate  = self._make_candidate()

        #4辺の形状判定結果
        self.unevens=[]
        for curve_tf in self.curves_tf:
            self.unevens.append(self._get_uneven(curve_tf, 10))
        
        #形状種類の判定結果
        self.shapetype = self._check_shapetype(self.unevens)

    #%% 形状候補の生成
    def _make_candidate(self):
        """
        Returns
        -------
        res　: 全てのstraight,convex,concaveのパターンを作成

        """
        
        seq = ["straight","convex","concave"]
        candidate_all=[]
        candidate=[]
        
        #全リストの生成
        for i in itertools.product(seq,repeat=4):
            candidate_all.append(list(i))
        
        #回転して重複したものを除去
        for idx,i in enumerate(candidate_all):
            for j in range(4):
                #並べ替えデータ
                tmp = i[:-1]
                tmp.insert(0,i[-1])
                #あるかのチェック
                if tmp in candidate_all[:idx]:
                    break
            else:
                candidate.append(tmp)
    
        return candidate


    #%%凹凸情報の取得
    def _get_uneven(self,data,thresh=10):
        """
        Parameters
        ----------
        data : カーブ
        thresh　：　直線と認識する閾値
        
        Returns
        -------
        res　: 判定結果 (直線：straight、凸：convex、凹：concave)
               
        """
        y = data[:,1]
        
        y_abs = np.abs(y)
        idx   = np.argmax(y_abs)
        
        height = y[idx]
        
        #分類わけ
        if max(y_abs) < thresh: #高さが5以下なら直線
            uneven = "straight"
        elif height > 0:
            uneven = "convex"
        else:
            uneven = "concave"
        return uneven

    #%%形状タイプのチェック
    def _check_shapetype(self,unevens):
        """
        Parameters
        ----------
        unevens　　　　　 ：　4辺の形状のリスト
        
        Returns
        -------
        res　: パターン判定結果のインデックス

        """
        for idx,i in enumerate(self.candidate):
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

