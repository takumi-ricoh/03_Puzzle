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
                        
                        #形状による絞り込みフラグ
                        match_type = self._get_shapetype_match(piece1,i,piece2,j)
                        
                        #いろいろなスコアzz
                        score1 = self._calc_MatchShapes_score(piece1,i,piece2,j)
                        score2 = self._calc_lengthS_score(piece1,i,piece2,j)
                        score3 = self._calc_lengthC_score(piece1,i,piece2,j)                        
                        
                        tmp.append([idx1,i,idx2,j,match_type,score1,score2,score3])
 
                #基準とする1辺ごとに、96個の確認結果をnp.arrayとし、それをリスト保存する
                res.append(np.array(tmp))
                tmp=[]
        return res


    #%%各辺の最適な組み合わせを確認し保存する
    def _get_best_matches(self,all_scores):
        res= []
        for score in all_scores:
            #形状が該当するもののみ抽出
            type_bool = score[:,4]==1
            tmp = score[type_bool]

            #直線による絞り込み
            if 5 < int(len(tmp)):
                num1 = 5
            else:
                num1 = int(len(tmp))
            
            idx1=np.argsort(tmp[:,6]) #6列目でソート
            tmp1=tmp[idx1,:][1:num1]
            
            
            #曲線による絞り込み
            if 3 < int(len(tmp1)):
                num2 = 3
            else:
                num2= int(len(tmp1))
                
            idx2=np.argsort(tmp1[:,7]) #7列目でソート
            tmp2=tmp1[idx2,:][1:num2]            
            
            #MatchShapesによる選択            
            idx = np.argmin(tmp2[:,5])

            #該当行を抽出
            match = tmp2[idx,:]

            #リスト保存
            res.append(match)        
        return res
        

    #%%エッジ種類によるマッチング                    
    def _get_shapetype_match(self,piece1,i,piece2,j):
        #比較する形状
        ref_type = piece1.shapetype.shapetype
        obj_type = piece2.shapetype.shapetype
        ref_unevens = piece1.shapetype.unevens[i]
        obj_unevens = piece2.shapetype.unevens[j]

        search_word = [ref_type, ref_unevens, obj_type, obj_unevens]
        
        candidate = [
                     #4 vs 16
                     [4,"convex",16,"concave"],
                     [16,"concave",4,"convex"],                     
                     #4 vs 11
                     [4,"concave",11,"convex"],
                     [11,"convex",4,"concave"],
                     #11 vs 16
                     [11,"concave",16,"convex"],
                     [16,"convex",11,"concave"],
                     #16 vs 11
                     [16,"concave",11,"convex"],
                     [11,"convex",16,"concave"],
                     #16 vs 31
                     [16,"convex",31,"concave"],
                     [31,"concave",16,"convex"],  
                     #11 vs 31
                     [11,"concave",31,"convex"],
                     [31,"convex",11,"concave"],
                     #31 vs 31
                     [31,"concave",31,"convex"],
                     [31,"convex",31,"concave"],]

        #候補があればOK
        if search_word in candidate:
            match = True

        #直線ならOK            
        elif ref_unevens=="straight":
            match = True
            
        #他の組み合わせはない    
        else:
            match = False

        return match

    #%%MatchShapes関数によるマッチング
    def _calc_MatchShapes_score(self,piece1,i,piece2,j):
        ref = piece1.edges.curves_img[i]
        obj = piece2.edges.curves_img[j]
        score = cv2.matchShapes(ref, obj, 1, 0.0)
        
        return score
    
    #%%直線距離による比較
    def _calc_lengthS_score(self,piece1,i,piece2,j):
        ref = piece1.edges.lens_straight[i]
        obj = piece2.edges.lens_straight[j]
        score = np.abs(ref - obj)
        
        return score

    #%%直線距離による比較
    def _calc_lengthC_score(self,piece1,i,piece2,j):
        ref = piece1.edges.lens_curve[i]
        obj = piece2.edges.lens_curve[j]
        score = np.abs(ref - obj)
        
        return score