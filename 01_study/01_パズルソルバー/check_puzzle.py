#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy
import cv2
import numpy as np
from datetime import datetime
import wx

""" Require OpenCV 3.0
     cv2.boxPointsが3.0以上を要求します
     
     pythonのバージョンが3.4じゃないとEnumが使えない！
     
     更新日 2017年11月7日
"""

class SolvePuzzle():
    """ まだテスト中
        切り出す対象の画像と、輪郭情報を引数にインスタンス化したい
    """
    def __init__(self, remove_bg, contours):
        self.__WINDOW_NAME = "AWEM solve"
        self.__WINDOW_X = 900
        self.__WINDOW_Y = 75
        self.__WINDOW_WIDTH = 320
        self.__WINDOW_HEIGHT = 320
        
        # 映像を出力するサブウインドウ
        cv2.namedWindow(self.__WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.__WINDOW_NAME, self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT)
        cv2.moveWindow(self.__WINDOW_NAME, self.__WINDOW_X, self.__WINDOW_Y)
        
        cv2.imshow(self.__WINDOW_NAME, remove_bg)
        
class CheckPuzzle():
    
    """ コンストラクタ
    """
    def __init__(self, cv_image):
        
        """ インスタンス変数
            self.__hoge と、__が書かれた変数はPrivate化されるようだ
        """
        self.SAVE_DIRPATH = "/media/tenderhope/08B3-ED90/capture/"
        self.MAIN_WINDOW_X = 75
        self.MAIN_WINDOW_Y = 75
        self.MAIN_WINDOW_WIDTH = 800
        self.MAIN_WINDOW_HEIGHT = 600
        
        self.__NODE_NAME = "AWEM Main"
        self.__imagetype = {"origin_image":cv_image, "L_image":None, "a_image":None, "b_image":None, \
                            "binary_image":None, "contours_image":None, "remove_bg":None}
        self.__mouseEvent = {"drag_start":None}
        self.__nowGaussianBlur = False
        self.__nowImage = None
        
        # パズル設定
        self.PUZZLE_MAXSIZE = 20000
        self.PUZZLE_MINSIZE = 10000
        self.contours = None                # 輪郭情報
        self.shutdown = None                # ESCまたはqが押されたかどうか
        self.removeSmallContours = True     # 小さい輪郭を削除するかどうか
        
        # 画像処理後の映像を出力するメインウインドウ
        cv2.namedWindow(self.__NODE_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.__NODE_NAME, self.MAIN_WINDOW_WIDTH, self.MAIN_WINDOW_HEIGHT)
        cv2.moveWindow(self.__NODE_NAME, self.MAIN_WINDOW_X, self.MAIN_WINDOW_Y)
        #cv2.createButton("Origin", self.callbackButton, "Origin", cv2.QT_RADIOBOX)
        
        # メインウインドウに対するマウスイベントを定義
        cv2.setMouseCallback(self.__NODE_NAME, self.__on_mouse_click, None)
        
        # デバッグ用のウインドウ
        cv2.namedWindow("TEST!!", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("TEST!!", 200, 200)
        
 
    def check(self):
    """ checkが呼ばれて初めて画像処理を実行する
    """ 
        # 画像処理
        # Lab色空間の各成分と、a成分の二値化像を作成
        self.__process_image(self.__imagetype["origin_image"])
        
        # 二値化像をコピー
        tmpImg = copy.copy(self.__imagetype["binary_image"])
        
        # アドレス先が異なっていることを確認
        #print id(self.__imagetype["binary_image"])
        #print id(tmpImg)
        
        # 輪郭検出
        # 一旦deepcopyしたものを渡す
        # tmpImgは書き換わってしまう点に注意
        self.__find_Contours(tmpImg)
    
    """ 画像処理の二値化部分
    """
    def __process_image(self, img1):
        
        # Lab色空間に分解
        lab_image = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
        
        self.__imagetype["L_image"] = lab_image[:, :, 0]
        self.__imagetype["a_image"] = lab_image[:, :, 1]
        self.__imagetype["b_image"] = lab_image[:, :, 2]
        
        # a成分に対してガウシアンフィルタをかけてから大津の二値化
        tmpImg = self.__mask_GaussianBlur("a_image", 1)
        ret3, th3 = cv2.threshold(tmpImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 二値化像を白黒反転
        invImg = 255 - th3
        
        # 画像のサイズを取得
        h, w = invImg.shape[:2]
        
        # 全成分がゼロの行列を作る
        mask = np.zeros((h+2, w+2), np.uint8)
        
        # 外側が
        cv2.floodFill(invImg, mask, (0, 0), 255);
        
        # 再反転
        # もし外側領域が無ければ、全白の画像になるはず
        invImg = 255 - invImg
        
        # マスク処理
        img_masked = cv2.bitwise_and(th3, th3, mask=invImg)
        
        # ノイズ除去
        kernel = np.ones((2,2),np.uint8)
        img_masked = cv2.morphologyEx(img_masked, cv2.MORPH_CLOSE, kernel)
        #img_masked = cv2.morphologyEx(img_masked, cv2.MORPH_OPEN, kernel)
        
        # 二値化像を格納
        self.__imagetype["binary_image"] = img_masked
        
        # パズル部分のみを白、背景を黒とした画像を格納
        remove_bg = cv2.bitwise_and(img1, img1, mask=img_masked)
        self.__imagetype["remove_bg"] = remove_bg
        
    """ ガウシアンフィルタをかける
    """
    def __mask_GaussianBlur(self, image_type, ave_size):
        
        # 平均化する画素の周囲の大きさを指定する。
        # (5, 5) の場合、個々の画素の地点の周囲5×5マスの平均をとる。
        # 数値が大きいほどぼやける。
        average_square = (ave_size, ave_size)
        
        # x軸方向の標準偏差
        sigma_x = 0
        
        image = self.__imagetype[image_type]
        
        try:
            if self.__nowGaussianBlur == False:
                image2 = cv2.GaussianBlur(image, average_square, sigma_x)
            else:
                image2 = image
                
            # マスクした画像を表示
            cv2.imshow(self.__NODE_NAME, image2)
            self.__nowGaussianBlur = not self.__nowGaussianBlur
            
        except:
            print "AWEM: Failed."
        
        return image2
    
    """ 輪郭検出
    """
    def __find_Contours(self, bin_img):
        # 輪郭検出 ３個の引数を必要とする関数です．
        # 第１引数は入力画像，
        # 第２引数はcontour retrieval mode，
        # 第３引数は輪郭検出方法を指定するフラグです．
        # 注意: OpenCV2ではcontoursとhierarchyの２つだけを返す
        _, contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        # 面積の大きい順にソート
        contours.sort(key=cv2.contourArea, reverse=True)
        
        # 小さいサイズの輪郭は削除
        if self.removeSmallContours:
            for i in reversed(range(0, len(contours))):
                if cv2.contourArea(contours[i]) < self.PUZZLE_MINSIZE:
                    contours.pop(i)
        
        # x座標の小さい順にソート
        contours.sort(key=cv2.boundingRect, reverse=False)
        
        # 注意：pythonは参照渡しで、
        # findContoursは入力画像を変更してしまうため、
        # コピーを値渡ししている
        tmpImg = copy.deepcopy(self.__imagetype["origin_image"])
        
        
        # BGRの順
        COLOR_BLUE = (255, 0, 0)
        COLOR_GREEN = (0, 255, 0)
        COLOR_RED = (0, 0, 255)
        
        LINE_SIZE = 2
        
        # やっぱりこいつも入力画像を描き換える…
        cv2.drawContours(tmpImg, contours, -1, COLOR_GREEN, LINE_SIZE)
        
        # 輪郭画像を格納
        self.__imagetype["contours_image"]  = tmpImg
        
        # 輪郭情報を格納
        self.contours = copy.copy(contours)
        
        #import pdb; pdb.set_trace()
        
        # 輪郭描画
        # 面積20000pix以下を表示する
        for i in range(0, len(contours)):
            area1 = cv2.contourArea(contours[i])
            
            if area1 < self.PUZZLE_MAXSIZE and area1 > self.PUZZLE_MINSIZE:
                # 重心計算
                M = cv2.moments(contours[i])
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                
                # 矩形計算
                x, y, w, h = cv2.boundingRect(contours[i])
                rect = cv2.minAreaRect(contours[i])
                center, size, angle = rect
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                
                text = str(i+1)
                
                # 重心に点を打つ
                cv2.circle(tmpImg, (cx, cy), LINE_SIZE, COLOR_RED, -1)
                
                # パズルNo.を書く
                cv2.putText(tmpImg, text, (cx+5, cy), cv2.FONT_HERSHEY_SIMPLEX, 1.3, COLOR_RED, LINE_SIZE)
                
                # 回転を考慮した外接矩形を描きたい
#                cv2.rectangle(tmpImg, (x,y), (x+w,y+h), COLOR_RED, LINE_SIZE)
                cv2.drawContours(tmpImg, [box], -1, COLOR_RED, LINE_SIZE)
                
                #-------------------------------------
                # 画像の切り出し 2017年11月07日追加
                #-------------------------------------
                
#                if i+1 == 4:
                tmpImg2 = copy.deepcopy(self.__imagetype["remove_bg"])
                
                # 画像のサイズを取得
                hhh, www = tmpImg2.shape[:2]
        
                # 全成分がゼロの行列を作る
                mask = np.zeros((hhh, www), np.uint8)
                
                cv2.drawContours(mask, contours, i, (255,255,255), -1)
                
                img_masked = cv2.bitwise_and(tmpImg2, tmpImg2, mask=mask)
                
#                if i+1 == 1:
#                    cv2.imshow("TEST!!", img_masked)
                
                roi = img_masked[y-25:y+h+25, x-25:x+w+25]
                center2 = tuple(np.array([roi.shape[1] * 0.5, roi.shape[0] * 0.5]))
                size = tuple(np.array([roi.shape[1], roi.shape[0]]))
                size = (250,250)
                rotation_matrix = cv2.getRotationMatrix2D(center2, angle, 1.0)
                
                # 回転した画像を生成
                img_rot = cv2.warpAffine(roi, rotation_matrix, size, flags=cv2.INTER_LINEAR)
                
                center2_x = center2[0]
                center2_y = center2[1]
                Mmm = np.float32([[1,0,125-center2_x],[0,1,125-center2_y]])
                size = (250,250)
                img_rot = cv2.warpAffine(img_rot, Mmm, size, flags=cv2.INTER_LINEAR)
                
                # 画像を書き出す
                #cv2.imwrite(self.SAVE_DIRPATH + str(i+1) + ".bmp", img_rot)
                
            else:
                cv2.drawContours(tmpImg, contours[i], -1, COLOR_BLUE, LINE_SIZE+3)
            
    """ 画像をメインウインドウに表示
    """
    def show(self, image_type):
        try:
            cv2.imshow(self.__NODE_NAME, self.__imagetype[image_type])
            cv2.displayOverlay(self.__NODE_NAME, image_type, 500)
        except:
            print "AWEM: Image show failed."
            
    """ 画像を保存
    """
    def save(self):
        basename = datetime.now().strftime("%Y%m%d%H%M%S")
        
        #cv2.imwrite(self.SAVE_DIRPATH + basename + "_Lab_L.bmp", self.__imagetype["L_image"])
        #cv2.imwrite(self.SAVE_DIRPATH + basename + "_Lab_a.bmp", self.__imagetype["a_image"])
        #cv2.imwrite(self.SAVE_DIRPATH + basename + "_Lab_b.bmp", self.__imagetype["b_image"])
        cv2.imwrite(self.SAVE_DIRPATH + basename + ".bmp", self.__imagetype["origin_image"])
        cv2.imwrite(self.SAVE_DIRPATH + basename + "_binary.bmp", self.__imagetype["binary_image"])
        cv2.imwrite(self.SAVE_DIRPATH + basename + "_remove.bmp", self.__imagetype["remove_bg"])
        cv2.imwrite(self.SAVE_DIRPATH + basename + "_contours.jpg", self.__imagetype["contours_image"])
        
        print "AWEM: Save image. -> " + self.SAVE_DIRPATH
        
    """ マウスイベントを定義
    """
    def __on_mouse_click(self, event, x, y, flags, param):
        
        # 一旦ローカル変数に格納
        drag_start = self.__mouseEvent["drag_start"]
        
        # 左クリックがあったらクリック座標をprint
        # 1回だけ認識してほしいので drag_start を使って判定
        if event == cv2.EVENT_LBUTTONDOWN and not drag_start:
            drag_start = (x, y)
            #nowImg = self.__imagetype[image_type]
            #px = nowImg[cv_image.getY(), cv_image.getX()]
            #print "AWEM: Clicked x={0:4d}, y={0:4d}".format(x).format(y)
            
        if event == cv2.EVENT_LBUTTONUP:
            drag_start = None
                
        self.__mouseEvent["drag_start"] = drag_start
    
    """ ウインドウイベントを定義
        キーボード入力を受け付ける
    """
    def keywait(self, wait_time):
    
        keystroke = cv2.waitKey(wait_time) & 0xff
        
        if keystroke == 27 or keystroke == ord("q"):
            self.shutdown = True
            cv2.destroyAllWindows()
            print "AWEM: Shut down..."
            
        elif keystroke == ord("o"):
            image_type = "origin_image"
            self.__nowImage = image_type
            self.show(image_type)
            
        elif keystroke == ord("l"):
            image_type = "L_image"
            self.__nowImage = image_type
            self.show(image_type)
            
        elif keystroke == ord("a"):
            image_type = "a_image"
            self.__nowImage = image_type
            self.show(image_type)
            
        elif keystroke == ord("b"):
            image_type = "b_image"
            self.__nowImage = image_type
            self.show(image_type)
        
        elif keystroke == ord("2"):
            image_type = "binary_image"
            self.__nowImage = image_type
            self.show(image_type)
        
        elif keystroke == ord("c"):
            image_type = "contours_image"
            self.__nowImage = image_type
            self.show(image_type)
        
        elif keystroke == ord("r"):
            image_type = "remove_bg"
            self.__nowImage = image_type
            self.show(image_type)
        
        elif keystroke == ord("p"):
            print "--------------------------------"
            for i in range(0, len(self.contours)):
                print " puzzle{0:02d} Area={1:7.1f}, Len={2:3d}".format(i+1, \
                    cv2.contourArea(self.contours[i]), len(self.contours[i]), )
            print "--------------------------------"
        
        elif keystroke == ord("s"):
            self.save()
        
        """
        elif keystroke == ord("g"):
            self.mask_GaussianBlur(image_type, 1)
            print "AWEM: Mask GaussianBlur -> " + str(self.__nowGaussianBlur)
        """
        
    """ 背景を黒色化した画像を返すプロパティっぽいやつ
    """
    #def getRemoveBgImage(self): return self.__imagetype["remove_bg"]
    
    def getImage(self, image_type):
        #print image_type
        return self.__imagetype[image_type]
    
    def getNowImage(self):
        return self.__nowImage
    
def main(args):
    try:
        
        # Class CheckPuzzleは初期化時に画像の絶対パスが必要
        # 画像を読み込み、画像処理実行
        BMP_PATH = "/media/tenderhope/08B3-ED90/capture/0923-1.bmp"
        
        AWEM = CheckPuzzle(cv2.imread(BMP_PATH))
        
        # 画像処理を実施し、パズルを抽出
        AWEM.check()
        
        print "AWEM: Start system."
        
        # image_type で使用可能なkey
        # origin_image   : 元画像像
        # L_image        : Lab色空間のL成分像
        # a_image        : Lab色空間のa成分像
        # b_image        : Lab色空間のb成分像
        # binary_image   : 二値化像
        # contours_image : 認識したパズルの重心、通し番号、矩形    
        # remove_bg      : 背景を黒にした元画像    
        # 画像を表示
        AWEM.show("origin_image")
        
        # AWEM.contoursに輪郭情報を格納している
        print "AWEM: Find {0} puzzles.".format(len(AWEM.contours))
        
        # デバッグ
        # パズル数が一致した場合の処理
        if len(AWEM.contours) == 24:
            #clip = SolvePuzzle(AWEM.getRemoveBgImage(), AWEM.contours)
            pass
            
        # キー入力を待機する無限ループ
        # ESC(27)またはqが押された場合は終了
        while True:
            AWEM.keywait(10)        
            if AWEM.shutdown == True:
                break
            
    except KeyboardInterrupt:
        print "AWEM: Shutting down vision node."
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)


