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

        #形状候補の取得
        self.candidate  = self._make_candidate()

class ShapeTypes():
    
    
    def __init__(self, edges):
        #形状候補の取得
        self.candidate  = self._make_candidate()

        #4辺の形状判定結果
        c0    =  Uneven(self.candidate, edges.edges[0])
        c1    =  Uneven(self.candidate, edges.edges[1])
        c2    =  Uneven(self.candidate, edges.edges[2])
        c3    =  Uneven(self.candidate, edges.edges[3])              

        #4辺の初期状態取得
        self.unevens = {"up":c0,"left":c1,"down":c2,"right":c3}
        
        self.shapetype = self._check_shapetype()      

    #%% 形状候補の生成
    def _make_candidate(self):
        """
        Returns
        -------
        res　: 全てのstraight,convex,concaveのパターンを作成

        """
        #回転
        def rot(data):
            res = data.copy()
            res["up"]    = data["left"]
            res["left"]  = data["down"]        
            res["down"]  = data["right"]        
            res["right"] = data["up"]   
            return res
        
        #全リストの生成
        seq = ["straight","convex","concave"]
        keys = ["up","left","down","right"]
        candidate_all=[]
        for value in itertools.product(seq,repeat=4):
            dic = dict(zip(keys, value))
            candidate_all.append(dic)
        
        #回転して重複したものを除去
        candidate=[]
        for cand in enumerate(candidate_all):
            for j in range(4):
                #回転
                key = rot(cand)
                #
                if key in candidate_all
                
                
                
                tmp.insert(0,i[-1])
                #あるかのチェック
                if tmp in candidate_all[:idx]:
                    break
            else:
                candidate.append(tmp)
    
        return candidate

    #%%形状タイプのチェック
    def _check_shapetype(self):
        """
        Parameters
        ----------
        unevens　　　　　 ：　4辺の形状のリスト
        
        Returns
        -------
        res　: パターン判定結果のインデックス

        """
        for j in range(4):
            #回転
            self._turn_cw()
            #一致するものがあれば、そのインデックス

        for idx,i in enumerate(self.candidate):
                            
                #回転
                self.edges._turn_cw()

                #一致するものがあれば、そのインデックス
                 
                tmp1 = tmp[:-1]
                tmp1.insert(0,tmp[-1])
                tmp = tmp1
                #チェック
                if tmp1 == i:
                    #print(tmp1)
                    return idx
                    break
                









