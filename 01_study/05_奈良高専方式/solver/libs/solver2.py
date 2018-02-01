# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 01:33:12 2018

@author: takumi
"""

import numpy as np
import cv2

class PuzzleSolver():

    MATCHSHAPE_ALGO = 1
    
    def __init__(self,pieceinfo_list):
        self.pieceinfo_list = pieceinfo_list

        self.result = np.empty((4,6))
        
        self._set_corner()
        
        
    def _set_corner(self):
        #shpaetypeが4のピースのみ抽出
        self.tmp = [i for i in self.pieceinfo_list if i.shapetype == 5]
        
        #shpaetypeが4のピースのみ抽出



        
    #%%すべての辺の組み合わせを確認し保存する
    def _get_all_matches(self, piecelist1, piecelist2):
        res=[]#結果
        tmp=[]        
        #基準のピース/辺のループ
        for idx1, piece1 in enumerate(piecelist1):
            for i in range(4):
           
                #比較するピース/辺のループ
                for idx2,piece2 in enumerate(piecelist2):
                    for j in range(4):
                        
                        #形状による絞り込みフラグ
                        match_type = self._get_shapetype_match(piece1,idx1,i,piece2,idx2,j)
                        
                        #いろいろなスコア
                        score1 = self._calc_MatchShapes_score(piece1,i,piece2,j,0)
                        score2 = self._calc_MatchShapes_score(piece1,i,piece2,j,1)
                        score3 = self._calc_MatchTemplate_score(piece1,i,piece2,j)                        
                        score4 = self._calc_lengthS_score(piece1,i,piece2,j)
                        score5 = self._calc_lengthC_score(piece1,i,piece2,j)                        
                        
                        tmp.append([idx1,i,idx2,j,match_type,score1,score2,score3,score4,score5])
 
                #基準とする1辺ごとに、96個の確認結果をnp.arrayとし、それをリスト保存する
                res.append(np.array(tmp))
                tmp=[]
        return res


    #%%各辺の最適な組み合わせを確認し保存する
    def _get_best_matches(self,all_matches):
        res= []
        for match in all_matches:
            #形状が該当するもののみ抽出
            type_bool = match[:,4]==1
            tmp1 = match[type_bool,:]

            #絞り込み
#            if 10 < int(len(tmp)):
#                num1 = 10
#            else:
#                num1 = int(len(tmp)/2)
#            
#            idx1=np.argsort(tmp[:,5]) #6列目でソート
#            tmp1=tmp[idx1,:][1:num1]
            
            
#            #曲線による絞り込み
#            if 3 < int(len(tmp1)):
#                num2 = 3
#            else:
#                num2= int(len(tmp1)/2)
#                
#            idx2=np.argsort(tmp1[:,7]) #7列目でソート
#            tmp2=tmp1[idx2,:][1:num2]            
            
            #MatchShapesによる選択            
            idx = np.argmax(tmp1[:,7])

            #該当行を抽出
            best = tmp1[idx,:]

            #リスト保存
            res.append(best)        
        return res
        

    #%%エッジ種類によるマッチング                    
    def _get_shapetype_match(self,piece1,idx1,i,piece2,idx2,j):
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

        #自分自身とはNG
        if idx1 == idx2:
            match = False

        #候補があればOK
        elif search_word in candidate:
            match = True

        #直線ならOK            
        elif ref_unevens=="straight":
            match = True
            
        #他の組み合わせはない    
        else:
            match = False

        return match

    #%%MatchShapes関数によるマッチング
    def _calc_MatchShapes_score(self,piece1,i,piece2,j,mode=0):
        
        if mode==0:
            ref = piece1.edges.curves_img2[i]
            obj = piece2.edges.curves_img2[j]

        else:
            ref = piece1.edges.curves_img_dil[i]
            obj = piece2.edges.curves_img_dil[j]
        
        algo = PuzzleSolver.MATCHSHAPE_ALGO

        score = cv2.matchShapes(ref, obj, algo, 0.0)
        
        return score

    #%%MatchSTemplate関数によるマッチング
    def _calc_MatchTemplate_score(self,piece1,i,piece2,j):
        
        ref = piece1.edges.curves_img_dil[i]
        obj = piece2.edges.curves_img_dil[j]
        
        #objの画像サイズ拡大
        base =np.zeros([500,500])
        size = obj.shape
        base[(250-size[1]):(250+size[1]),(250-size[0]):(250+size[0])]=255
        base=base.astype(np.uint8)
        
        match = cv2.matchTemplate(base, ref, cv2.TM_SQDIFF)
        min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)

        score = min_value
        
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