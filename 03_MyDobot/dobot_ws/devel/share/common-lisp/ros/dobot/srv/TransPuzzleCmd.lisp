; Auto-generated. Do not edit!


(cl:in-package dobot-srv)


;//! \htmlinclude TransPuzzleCmd-request.msg.html

(cl:defclass <TransPuzzleCmd-request> (roslisp-msg-protocol:ros-message)
  ((src_x
    :reader src_x
    :initarg :src_x
    :type cl:float
    :initform 0.0)
   (src_y
    :reader src_y
    :initarg :src_y
    :type cl:float
    :initform 0.0)
   (dst_x
    :reader dst_x
    :initarg :dst_x
    :type cl:float
    :initform 0.0)
   (dst_y
    :reader dst_y
    :initarg :dst_y
    :type cl:float
    :initform 0.0))
)

(cl:defclass TransPuzzleCmd-request (<TransPuzzleCmd-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TransPuzzleCmd-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TransPuzzleCmd-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dobot-srv:<TransPuzzleCmd-request> is deprecated: use dobot-srv:TransPuzzleCmd-request instead.")))

(cl:ensure-generic-function 'src_x-val :lambda-list '(m))
(cl:defmethod src_x-val ((m <TransPuzzleCmd-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dobot-srv:src_x-val is deprecated.  Use dobot-srv:src_x instead.")
  (src_x m))

(cl:ensure-generic-function 'src_y-val :lambda-list '(m))
(cl:defmethod src_y-val ((m <TransPuzzleCmd-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dobot-srv:src_y-val is deprecated.  Use dobot-srv:src_y instead.")
  (src_y m))

(cl:ensure-generic-function 'dst_x-val :lambda-list '(m))
(cl:defmethod dst_x-val ((m <TransPuzzleCmd-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dobot-srv:dst_x-val is deprecated.  Use dobot-srv:dst_x instead.")
  (dst_x m))

(cl:ensure-generic-function 'dst_y-val :lambda-list '(m))
(cl:defmethod dst_y-val ((m <TransPuzzleCmd-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dobot-srv:dst_y-val is deprecated.  Use dobot-srv:dst_y instead.")
  (dst_y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TransPuzzleCmd-request>) ostream)
  "Serializes a message object of type '<TransPuzzleCmd-request>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'src_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'src_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'dst_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'dst_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TransPuzzleCmd-request>) istream)
  "Deserializes a message object of type '<TransPuzzleCmd-request>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'src_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'src_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'dst_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'dst_y) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TransPuzzleCmd-request>)))
  "Returns string type for a service object of type '<TransPuzzleCmd-request>"
  "dobot/TransPuzzleCmdRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TransPuzzleCmd-request)))
  "Returns string type for a service object of type 'TransPuzzleCmd-request"
  "dobot/TransPuzzleCmdRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TransPuzzleCmd-request>)))
  "Returns md5sum for a message object of type '<TransPuzzleCmd-request>"
  "80257a33fbe8eda7e69a8ee2a7a08d79")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TransPuzzleCmd-request)))
  "Returns md5sum for a message object of type 'TransPuzzleCmd-request"
  "80257a33fbe8eda7e69a8ee2a7a08d79")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TransPuzzleCmd-request>)))
  "Returns full string definition for message of type '<TransPuzzleCmd-request>"
  (cl:format cl:nil "float32 src_x~%float32 src_y~%float32 dst_x~%float32 dst_y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TransPuzzleCmd-request)))
  "Returns full string definition for message of type 'TransPuzzleCmd-request"
  (cl:format cl:nil "float32 src_x~%float32 src_y~%float32 dst_x~%float32 dst_y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TransPuzzleCmd-request>))
  (cl:+ 0
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TransPuzzleCmd-request>))
  "Converts a ROS message object to a list"
  (cl:list 'TransPuzzleCmd-request
    (cl:cons ':src_x (src_x msg))
    (cl:cons ':src_y (src_y msg))
    (cl:cons ':dst_x (dst_x msg))
    (cl:cons ':dst_y (dst_y msg))
))
;//! \htmlinclude TransPuzzleCmd-response.msg.html

(cl:defclass <TransPuzzleCmd-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:integer
    :initform 0))
)

(cl:defclass TransPuzzleCmd-response (<TransPuzzleCmd-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TransPuzzleCmd-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TransPuzzleCmd-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dobot-srv:<TransPuzzleCmd-response> is deprecated: use dobot-srv:TransPuzzleCmd-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <TransPuzzleCmd-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dobot-srv:result-val is deprecated.  Use dobot-srv:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TransPuzzleCmd-response>) ostream)
  "Serializes a message object of type '<TransPuzzleCmd-response>"
  (cl:let* ((signed (cl:slot-value msg 'result)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TransPuzzleCmd-response>) istream)
  "Deserializes a message object of type '<TransPuzzleCmd-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'result) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TransPuzzleCmd-response>)))
  "Returns string type for a service object of type '<TransPuzzleCmd-response>"
  "dobot/TransPuzzleCmdResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TransPuzzleCmd-response)))
  "Returns string type for a service object of type 'TransPuzzleCmd-response"
  "dobot/TransPuzzleCmdResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TransPuzzleCmd-response>)))
  "Returns md5sum for a message object of type '<TransPuzzleCmd-response>"
  "80257a33fbe8eda7e69a8ee2a7a08d79")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TransPuzzleCmd-response)))
  "Returns md5sum for a message object of type 'TransPuzzleCmd-response"
  "80257a33fbe8eda7e69a8ee2a7a08d79")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TransPuzzleCmd-response>)))
  "Returns full string definition for message of type '<TransPuzzleCmd-response>"
  (cl:format cl:nil "int32 result~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TransPuzzleCmd-response)))
  "Returns full string definition for message of type 'TransPuzzleCmd-response"
  (cl:format cl:nil "int32 result~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TransPuzzleCmd-response>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TransPuzzleCmd-response>))
  "Converts a ROS message object to a list"
  (cl:list 'TransPuzzleCmd-response
    (cl:cons ':result (result msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'TransPuzzleCmd)))
  'TransPuzzleCmd-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'TransPuzzleCmd)))
  'TransPuzzleCmd-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TransPuzzleCmd)))
  "Returns string type for a service object of type '<TransPuzzleCmd>"
  "dobot/TransPuzzleCmd")