#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import sys
import cv2
import numpy as np
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
from ros_start.check_puzzle import CheckPuzzle

class AwemMain():
    def __init__(self):
    
        self.nowImage = "contours_image"
        self.NUMBER_OF_PIECES = 24
        self.checkSum = False
        self.__waitTime = 200
        
        rospy.on_shutdown(self.__cleanup)
        
        # OpenCVとROSのMessage(sensor_msgs/Image)を変換するコンバータ
        self.bridge = CvBridge()
        
        # クラスの初期化時に必要な"Publisher"と"Subscriber"を作る
        self.image_pub = rospy.Publisher("Origin_image", Image, queue_size=1)
        
        # 入力としての画像
        # input_rgb_imageという名前で、sensor_msgs/Image型のTopicをSubscribe
        # 受信したデータに対してimage_callbackという関数を実行する
        self.image_sub = rospy.Subscriber("input_rgb_image", Image, self.__image_callback, queue_size=1)
    
    """ コールバック
        Subscriberが受信したデータに対して実行する
    """
    def __image_callback(self, ros_image):
        try:
            # CvBridgeを使ってMessageをOpenCVの画像形式に変換
            # 赤青が反転している場合はrgb8などに変えてみる
            cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError, e:
            print e
        
        # class check_puzzleのインスタンス
        awemtest = CheckPuzzle(cv_image)
        
        awemtest.check()
        
        if len(awemtest.contours) == self.NUMBER_OF_PIECES and not self.checkSum:
            print "AWEM: Find {0:d} pieces.".format(self.NUMBER_OF_PIECES)
            #awemtest.save()
            self.checkSum = True
            #self.__waitTime = 0     # 画像描画を止める
            
        # image_type で使用可能なkey
        # origin_image   : 元画像像
        # L_image        : Lab色空間のL成分像
        # a_image        : Lab色空間のa成分像
        # b_image        : Lab色空間のb成分像
        # binary_image   : 二値化像
        # contours_image : 認識したパズルの重心、通し番号、矩形  
        
        # 画像を表示
        # 何を写すかは self.nowImage で管理
        awemtest.show(self.nowImage)
        
        process_image = awemtest.getImage(self.nowImage)
        
        if self.nowImage == "origin_image" or self.nowImage == "contours_image":
            encoding = "bgr8"
        elif self.nowImage == "remove_bg":
            encoding = "bgr8"
        else:
            encoding = "mono8"
        
        # デバッグ用に画像処理した画像をPublishしておく
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(process_image, encoding))
        
        # 100msごとにキーボード操作を監視し、無限ループ
        awemtest.keywait(self.__waitTime)
        
        # キーボードイベントを取得し、画像変更だった場合の処理
        if awemtest.getNowImage() <> None:
            self.nowImage = awemtest.getNowImage()
        
    def __cleanup(self):
        print "Shutting down vision node."
        cv2.destroyAllWindows()
        
def main(args):

    rospy.init_node("AWEM Main")
    AwemMain()
    
    try:    
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vision node."
        cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
