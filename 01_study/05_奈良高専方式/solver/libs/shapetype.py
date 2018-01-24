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
    
    def __init__(self, edges):
        #形状候補の取得
        self.candidate  = self._make_candidate()

        #4辺の形状
        left  = edges.left.uneven
        up    = edges.up.uneven
        right = edges.right.uneven
        down  = edges.down.uneven

        unevens = [left, up, right, down]
        
        self.shapetype = self._check_shapetype(unevens)

    #%% 形状候補の生成
    def _make_candidate(self):

        #全リストの生成
        seq = ["straight","convex","concave"]
        candidate_all=[]
        for i in itertools.product(seq,repeat=4):
            candidate_all.append(i)
        
        #回転して重複したものを除去
        candidate=[]
        for cand in enumerate(candidate_all):
            #4回回す
            for j in range(4):
                #回転する
                cand = cand[-1:] + cand[:-1]
                #もしすでに候補にあればやめる
                if cand in candidate:
                    break
            else:
                candidate.append(cand) #最後まで行ったら追加
                    
        return candidate


    #%%形状タイプのチェック
    def _check_shapetype(self, unevens):
        res = 100000
        
        for j in range(4):
            #回転
            unevens = unevens[-1:] + unevens[:-1]
            #該当パターンのインデックスを返す
            if unevens in self.candidate:
                res = self.candidate.index(unevens)
                break
        
        return res