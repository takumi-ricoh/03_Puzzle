# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 23:58:25 2018

@author: takumi
"""
import numpy as np
import cv2

class PuzzleSolver():

    MATCHSHAPE_ALGO = 1
    
    def __init__(self,pieceinfo_list):
        #初期化
        self.plist   = pieceinfo_list
        #すべての組み合わせスコア計算
        self.all_matches = self._get_all_matches(self.plist)
        #基準1辺ごとに最適な辺を選択
        self.match_res  = self._get_best_matches(self.all_matches) 
        #4辺ずつ、サブリストに分割
        self.match_res_p = [self.match_res[x:x+4] for x in range(0, len(self.match_res), 4)]

    #%%すべての辺の組み合わせを確認し保存する
    def _get_all_matches(self, piecelist):
        res=[]#結果
        tmp=[]        
        #基準のピース/辺のループ
        for piece1 in piecelist:
            for key1,val1 in piece1.edges.items():
                uneven1 = val1.uneven
                img1 =  val1.curve_img2
                des1 = val1.fPoint_des
           
                #比較するピース/辺のループ
                for piece2 in piecelist:
                    for key2,val2 in piece1.edges.items():
                        uneven2 = val2.uneven
                        img2 =  val2.curve_img2
                        des2 = val2.fPoint_des
                        
                        #形状による絞り込みフラグ
                        match_type = self._get_shapetype_match(piece1,uneven1, piece2,uneven2)
                        
                        #MatchShapes関数によるスコア
                        score1 = self._calc_MatchShapes_score(img1,img2)
                        #Match関数によるスコア
                        score2 = self._calc_MatchTemplate_score(img1,img2)                        
                        #特徴量関数によるスコア
                        score3 = self._calc_MatchFeature_score(des1,des2)                       

                                   
                        tmp.append([piece1.var, key1, piece2.var, key2, match_type, score1, score2, score3])
 
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
            
            #最大のものを選択           
            idx = np.argmax(tmp1[:,7])

            #該当行を抽出
            best = tmp1[idx,:]

            #リスト保存
            res.append(best)        
            
        return res

    #%%エッジ種類によるマッチング                    
    def _get_shapetype_match(self,piece1,uneven1,piece2,uneven2):
        #比較する形状
        ref_type = piece1.shapetype
        obj_type = piece2.shapetype
        ref_uneven = uneven1
        obj_uneven = uneven2
        search_word = [ref_type, ref_uneven, obj_type, obj_uneven]
        
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
        if piece1.var == piece2.var:
            match = False

        #候補があればOK
        elif search_word in candidate:
            match = True

        #直線ならOK            
        elif ref_uneven=="straight":
            match = True
            
        #他の組み合わせはない    
        else:
            match = False

        return match

    #%%MatchShapes関数によるマッチング
    def _calc_MatchShapes_score(self,img1,img2):
        
        ref = img1
        obj = img2
        
        algo = PuzzleSolver.MATCHSHAPE_ALGO

        score = cv2.matchShapes(ref, obj, algo, 0.0)
        
        return score

    #%%MatchSTemplate関数によるマッチング
    def _calc_MatchTemplate_score(self,img1,img2):
        
        ref = img1
        obj = img2
        
        #objの画像サイズ拡大
        base =np.zeros([500,500])
        size = obj.shape
        base[(250-size[1]):(250+size[1]),(250-size[0]):(250+size[0])]=255
        base=base.astype(np.uint8)
        
        match = cv2.matchTemplate(base, ref, cv2.TM_SQDIFF)
        min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)

        score = min_value
        
        return score
    
    #%%MatchFeature関数によるマッチング
    def _calc_MatchFeature_score(self,des1,des2):
        
        #Brute=Force matcher
        bfm = cv2.BFMatcher(cv2.NORM_HAMMING)
        
        #マッチしたポイントのリスト
        match = bfm.match(des1,des2)
        
        #特徴点の距離の平均
        dist = [m.distance for m in match]
        score = sum(dist)/len(dist)

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