;; Auto-generated. Do not edit!


(when (boundp 'dobot::TransPuzzleCmd)
  (if (not (find-package "DOBOT"))
    (make-package "DOBOT"))
  (shadow 'TransPuzzleCmd (find-package "DOBOT")))
(unless (find-package "DOBOT::TRANSPUZZLECMD")
  (make-package "DOBOT::TRANSPUZZLECMD"))
(unless (find-package "DOBOT::TRANSPUZZLECMDREQUEST")
  (make-package "DOBOT::TRANSPUZZLECMDREQUEST"))
(unless (find-package "DOBOT::TRANSPUZZLECMDRESPONSE")
  (make-package "DOBOT::TRANSPUZZLECMDRESPONSE"))

(in-package "ROS")





(defclass dobot::TransPuzzleCmdRequest
  :super ros::object
  :slots (_src_x _src_y _dst_x _dst_y ))

(defmethod dobot::TransPuzzleCmdRequest
  (:init
   (&key
    ((:src_x __src_x) 0.0)
    ((:src_y __src_y) 0.0)
    ((:dst_x __dst_x) 0.0)
    ((:dst_y __dst_y) 0.0)
    )
   (send-super :init)
   (setq _src_x (float __src_x))
   (setq _src_y (float __src_y))
   (setq _dst_x (float __dst_x))
   (setq _dst_y (float __dst_y))
   self)
  (:src_x
   (&optional __src_x)
   (if __src_x (setq _src_x __src_x)) _src_x)
  (:src_y
   (&optional __src_y)
   (if __src_y (setq _src_y __src_y)) _src_y)
  (:dst_x
   (&optional __dst_x)
   (if __dst_x (setq _dst_x __dst_x)) _dst_x)
  (:dst_y
   (&optional __dst_y)
   (if __dst_y (setq _dst_y __dst_y)) _dst_y)
  (:serialization-length
   ()
   (+
    ;; float32 _src_x
    4
    ;; float32 _src_y
    4
    ;; float32 _dst_x
    4
    ;; float32 _dst_y
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _src_x
       (sys::poke _src_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _src_y
       (sys::poke _src_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _dst_x
       (sys::poke _dst_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _dst_y
       (sys::poke _dst_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _src_x
     (setq _src_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _src_y
     (setq _src_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _dst_x
     (setq _dst_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _dst_y
     (setq _dst_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(defclass dobot::TransPuzzleCmdResponse
  :super ros::object
  :slots (_result ))

(defmethod dobot::TransPuzzleCmdResponse
  (:init
   (&key
    ((:result __result) 0)
    )
   (send-super :init)
   (setq _result (round __result))
   self)
  (:result
   (&optional __result)
   (if __result (setq _result __result)) _result)
  (:serialization-length
   ()
   (+
    ;; int32 _result
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _result
       (write-long _result s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _result
     (setq _result (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass dobot::TransPuzzleCmd
  :super ros::object
  :slots ())

(setf (get dobot::TransPuzzleCmd :md5sum-) "80257a33fbe8eda7e69a8ee2a7a08d79")
(setf (get dobot::TransPuzzleCmd :datatype-) "dobot/TransPuzzleCmd")
(setf (get dobot::TransPuzzleCmd :request) dobot::TransPuzzleCmdRequest)
(setf (get dobot::TransPuzzleCmd :response) dobot::TransPuzzleCmdResponse)

(defmethod dobot::TransPuzzleCmdRequest
  (:response () (instance dobot::TransPuzzleCmdResponse :init)))

(setf (get dobot::TransPuzzleCmdRequest :md5sum-) "80257a33fbe8eda7e69a8ee2a7a08d79")
(setf (get dobot::TransPuzzleCmdRequest :datatype-) "dobot/TransPuzzleCmdRequest")
(setf (get dobot::TransPuzzleCmdRequest :definition-)
      "float32 src_x
float32 src_y
float32 dst_x
float32 dst_y
---
int32 result


")

(setf (get dobot::TransPuzzleCmdResponse :md5sum-) "80257a33fbe8eda7e69a8ee2a7a08d79")
(setf (get dobot::TransPuzzleCmdResponse :datatype-) "dobot/TransPuzzleCmdResponse")
(setf (get dobot::TransPuzzleCmdResponse :definition-)
      "float32 src_x
float32 src_y
float32 dst_x
float32 dst_y
---
int32 result


")



(provide :dobot/TransPuzzleCmd "80257a33fbe8eda7e69a8ee2a7a08d79")


