# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 23:58:25 2018

@author: takumi
"""
import numpy as np
import cv2

class PuzzleSolver():

    def __init__(self,pieceinfo_list):
        #初期化
        self.plist  = pieceinfo_list
        #すべての組み合わせスコア計算
        self.all_scores = self._get_all_matches(self.plist)
        #基準1辺ごとに最適な辺を選択
        self.match_res  = self._get_best_matches(self.all_scores) 
        #4辺ずつ、サブリストに分割
        self.match_res_p = zip(*[iter(self.match_res)]*4)

    #%%すべての辺の組み合わせを確認し保存する
    def _get_all_matches(self,piecelist):
        res=[]#結果
        tmp=[]        
        #基準のピース/辺のループ
        for idx1, piece1 in enumerate(piecelist):
            for i in range(4):
           
                #比較するピース/辺のループ
                for idx2,piece2 in enumerate(piecelist):
                    for j in range(4):
                        
                        #一つ一つ確認
                        match1 = self._get_shapetype_match(piece1,i,piece2,j)
                        score1 = self._get_MatchShapes_match(piece1,i,piece2,j)
                        
                        tmp.append([idx1,i,idx2,j,match1,score1])
 
                #基準とする1辺ごとに、96個の確認結果をnp.arrayとし、それをリスト保存する
                res.append(np.array(tmp))
                tmp=[]
        return res


    #%%各辺の最適な組み合わせを確認し保存する
    def _get_best_matches(self,all_scores):
        res= []
        for score in all_scores:
            #形状が該当するもののみ抽出
            tmp = score[score[:,4]==True]
            #この中でスコア最小となるインデックス    
            idx = np.argmin(tmp[:,5])
            #該当行を抽出
            match = tmp[idx,:]
            #リスト保存
            res.append(match)        
        return res
        

    #%%形状種類によるマッチング                    
    def _get_shapetype_match(self,piece1,i,piece2,j):
        #比較する形状
        ref_type = piece1.shapetype.unevens[i]
        obj_type = piece2.shapetype.unevens[j]

        #エッジ種類による比較
        if (ref_type=="convex") and (obj_type=="concave"):
            match = True
            
        elif (ref_type=="concave") and (obj_type=="convex"):
            match = True

        elif ref_type=="straight":
            match = True
            
        else:
            match = False

        return match


    #%%MatchShapes関数によるマッチング
    def _get_MatchShapes_match(self,piece1,i,piece2,j):
        ref = piece1.edges.curves_img[i]
        obj = piece2.edges.curves_img[j]
        score = cv2.matchShapes(ref, obj, 3, 0.0)
        
        return score
