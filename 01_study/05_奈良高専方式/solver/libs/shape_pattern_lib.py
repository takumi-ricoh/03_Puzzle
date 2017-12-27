# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 18:07:47 2017

@author: p000495138
"""
import numpy as np
import itertools

#%%凹凸情報の取得
def get_uneven(data,thresh):
    """
    Parameters
    ----------
    data : カーブ
    thresh　：　直線と認識する閾値
    
    Returns
    -------
    res　: 判定結果 (直線：straight、凸：convex、凹：concave)
    
    Notes
    -------
    yの絶対値が最大の場所が、マイナスか、プラスか、で判定
    
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





#%%チェックリスト生成
def make_all_shapepattern():
    """
    Parameters
    ----------
    無し
    
    Returns
    -------
    res　: 全てのstraight,convex,concaveのパターンを作成
    
    Notes
    -------
    無し 
    """
    
    seq = ["straight","convex","concave"]
    shape_pattern=[]
    shape_pattern2=[]
    
    #全リストの生成
    for i in itertools.product(seq,repeat=4):
        shape_pattern.append(list(i))
    
    #回転して重複したものを除去
    for idx,i in enumerate(shape_pattern):
        for j in range(4):
            #並べ替えデータ
            tmp = i[:-1]
            tmp.insert(0,i[-1])
            #あるかのチェック
            if tmp in shape_pattern[:idx]:
                break
        else:
            shape_pattern2.append(tmp)

    return shape_pattern2






#%%形状タイプのチェック
def check_shapetype(unevens,shape_pattern):
    """
    Parameters
    ----------
    unevens　　　　　 ：　4辺の形状のリスト
    shape_pattern ：　形状の候補　
    
    Returns
    -------
    res　: パターン判定結果のインデックス
    
    Notes
    -------
    無し 
    """
    for idx,i in enumerate(shape_pattern):
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
