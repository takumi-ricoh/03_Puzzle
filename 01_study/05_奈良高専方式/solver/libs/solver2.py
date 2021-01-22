# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 01:33:12 2018

@author: takumi
"""

import numpy as np
import cv2
import itertools
import timeit

#@jit
def loop(slist,list1,list2,list3):
    res = []
    for type5 in list1:
        for type11 in list2:
            for type15 in list3:                
                #1つの並びを完成させるループ
                tmp = []
                count5=0
                count11=0
                count15=0
                for idx,shape in enumerate(slist):
                    if shape == 5:
                        tmp.append(type5[count5])
                        count5 += 1 
                    elif shape == 11:
                        tmp.append(type11[count11])
                        count11 += 1
                    elif shape == 15:
                        tmp.append(type15[count15])
                        count15 += 1
                res.append(tmp)
    return res
    


class PuzzleSolver():

    MATCHSHAPE_ALGO = 1
    
    def __init__(self,pieceinfo_list):
        self.pieceinfo_list = pieceinfo_list

        self.slist=[5, 15,  11,  15,  11,  5, 15,  11,  5, 15,  11,  15,  11,  5, 15,  11]
        self.ulist=[0, "d", "d", "d", "d", 0, "r", "r", 0, "u", "u", "u", "u", 0, "l", "l"]
        
        self.cand_list =  timeit.timeit(self._get_cand())
    

    def _get_cand(self):
        #shpaetypeが4のピースのみ抽出
        self.type5  = [i.var for i in self.pieceinfo_list if i.shapetype == 5]
        self.type11 = [i.var for i in self.pieceinfo_list if i.shapetype == 11]
        self.type15 = [i.var for i in self.pieceinfo_list if i.shapetype == 15]
        #順列
        self.perm_type5  = list(itertools.permutations(self.type5))
        self.perm_type11 = list(itertools.permutations(self.type11))        
        self.perm_type15 = list(itertools.permutations(self.type15))
        
        res = print(timeit.timeit(loop(self.slist, self.perm_type5, self.perm_type11, self.perm_type15)))
        
#        res=[]
#        for idx,i in enumerate(self.typeallvar):
#            if list(self.typealltype[idx]) == self.slist[idx]:
#                var  = self.typeallvar[idx]
#                data = [i for i in self.pieceinfo_list if i.var == var] 
#                res.append(data[0])
        
        return res

"""
    #%%各辺の最適な組み合わせを確認し保存する
    def _get_best_matches(self,all_matches):
        res= []
        for match in all_matches:
            #形状が該当するもののみ抽出
            type_bool = match[:,4]==1
            tmp1 = match[type_bool,:]
            #MatchShapesによる選択            
            idx = np.argmax(tmp1[:,7])

            #該当行を抽出
            best = tmp1[idx,:]

            #リスト保存
            res.append(best)        
        return res
        
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
"""