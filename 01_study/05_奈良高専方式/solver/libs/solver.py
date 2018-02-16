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
#        #基準1辺ごとに最適な辺を選択
#        self.match_res  = self._get_best_matches(self.all_matches) 
#        #4辺ずつ、サブリストに分割
#        self.match_res_p = [self.match_res[x:x+4] for x in range(0, len(self.match_res), 4)]

    #%%すべての辺の組み合わせを確認し保存する
    def _get_all_matches(self, piecelist):
        res=[]#結果
        tmp=[]        
        #基準のピース/辺のループ
        for piece1 in piecelist:
            for key1,val1 in piece1.edges.items():
                uneven1 = val1.uneven
                img1 =  val1.curve_img2
                akaze1 = val1.akaze_des
                orb1 = val1.orb_des
                #sift1 = val1.sift_des
                ngb1 = piece1.edgesNgb[key1].uneven#時計方向隣の形状
           
                #比較するピース/辺のループ
                for piece2 in piecelist:
                    for key2,val2 in piece2.edges.items():
                        uneven2 = val2.uneven
                        img2 =  val2.curve_img2
                        akaze2 = val2.akaze_des
                        orb2   = val2.orb_des
                        #sift2  = val2.sift_des
                        ngb2   = piece2.edgesNgb[key2].uneven#時計回りとなりの形状
                        
                        #形状による絞り込みフラグ
                        match_type = self._get_shapetype_match(piece1,uneven1, piece2,uneven2,ngb1,ngb2)
                        
                        #MatchShapes関数によるスコア
                        score1 = self._calc_MatchShapes_score(img1,img2)
                        #Match関数によるスコア
                        score2 = self._calc_MatchTemplate_score(img1,img2)                        
                        
                        #特徴量関数によるスコア
                        if (uneven1=="straight")or(uneven2=="straight"):
                            score3=0
                            score4=0
                            #score5=0
                        else:
                            score3 = self._calc_MatchFeature_score(akaze1,akaze2)                       
                            score4 = self._calc_MatchFeature_score(orb1,orb2)
                            #score5 = self._calc_MatchFeature_score(sift1,sift2)
                        print(piece1.var,key1,piece2.var,key2,score3)
                                   
                        tmp.append([piece1.var, key1, uneven1,piece2.var, key2,uneven2, match_type,\
                                    score1, score2, score3, score4,])
 
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
    def _get_shapetype_match(self,piece1,uneven1,piece2,uneven2,ngb1,ngb2):
        #比較する形状
        ref_type = piece1.shapetype
        obj_type = piece2.shapetype
        ref_uneven = uneven1
        obj_uneven = uneven2
        obj_ngb = ngb2
        search_word = [ref_type, ref_uneven, obj_type, obj_uneven, obj_ngb]
        
        candidate = [
                     #4 vs 16
                     [5,"convex",15,"concave","convex"],
                     [15,"concave",5,"convex","straight"],                     
                     #4 vs 11
                     [5,"concave",11,"convex","straight"],
                     [11,"convex",5,"concave","convex"],
                     #16 vs 11
                     [15,"concave",11,"convex","concave"],
                     [11,"convex",15,"concave","straight"],
                     #16 vs 11
                     [15,"concave",11,"convex","straight"],
                     [11,"convex",15,"concave","convex"],

                     #15 vs 21
                     [15,"convex",21,"concave","convex"],
                     [21,"concave",15,"convex","concave"], 
                     
                     #11 vs 31
                     [11,"concave",21,"convex","concave"],
                     [21,"convex",11,"concave","convex"],
                     
                     #31 vs 31
                     [21,"concave",21,"convex","concave"],
                     [21,"convex",21,"concave","convex"],]

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
    
    #%%BGMatcher関数によるマッチング
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