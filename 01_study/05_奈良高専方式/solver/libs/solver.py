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
        self.match_res_p = [self.match_res[x:x+4] for x in range(0, len(self.match_res), 4)]

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
                        
                        #制約条件のフラグ
                        match1 = self._get_edgetype_match1(piece1,i,piece2,j)
                        match2 = self._get_shapetype_match1(piece1,piece2)
                        match3 = self._get_edgetype_match2(piece1,i,piece2,j)
                        #スコア
                        score1 = self._get_MatchShapes_match(piece1,i,piece2,j)
                        
                        tmp.append([idx1,i,idx2,j,match1,score1,match2,match3])
 
                #基準とする1辺ごとに、96個の確認結果をnp.arrayとし、それをリスト保存する
                res.append(np.array(tmp))
                tmp=[]
        return res


    #%%各辺の最適な組み合わせを確認し保存する
    def _get_best_matches(self,all_scores):
        res= []
        for score in all_scores:
            #形状が該当するもののみ抽出
            bool1 = score[:,4]==1
            bool2 = score[:,6]==1
            bool3 = score[:,7]==1
            bool_total = [min(t) for t in zip(bool1, bool2, bool3)]
            tmp = score[bool_total]
            #この中でスコア最小となるインデックス    
            idx = np.argmin(tmp[:,5])
            #該当行を抽出
            match = tmp[idx,:]
            #リスト保存
            res.append(match)        
        return res
        

    #%%エッジ種類によるマッチング                    
    def _get_edgetype_match1(self,piece1,i,piece2,j):
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

    #%%形状種類によるマッチング(直線を含むか)                   
    def _get_shapetype_match1(self,piece1,piece2):
        #比較する形状
        ref_type = piece1.shapetype.shapetype
        obj_type = piece2.shapetype.shapetype

        #同一形状を除去
        if ref_type == obj_type:
            match = False
         
        #4と31の組み合わせ除去
        elif (ref_type==4) and (obj_type==31):
            match = False

        elif (ref_type==31) and (obj_type==4):
            match = False
            
        else:
            match = True

        return match
    
    #%%形状種類によるマッチング(type31の辺は、隣に直線のある辺とはつかない)                   
    def _get_edgetype_match2(self,piece1,i,piece2,j):
        
        #リファレンス
        ref_next = piece1.shapetype.next_not_straight[i]
        ref_type = piece1.shapetype.shapetype

        #対象の
        obj_next = piece2.shapetype.next_not_straight[j]
        obj_type = piece2.shapetype.shapetype
        
        #31 vs 隣に直線ががあるかどうか
        if (ref_type==31) and (obj_next==False):
            match = False

        elif (ref_next==False) and (obj_type==31):
            match = False
            
        else:
            match = True

        return match

    #%%MatchShapes関数によるマッチング
    def _get_MatchShapes_match(self,piece1,i,piece2,j):
        ref = piece1.edges.curves_img[i]
        obj = piece2.edges.curves_img[j]
        score = cv2.matchShapes(ref, obj, 1, 0.0)
        
        return score
