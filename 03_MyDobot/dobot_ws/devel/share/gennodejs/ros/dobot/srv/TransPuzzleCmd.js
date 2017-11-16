// Auto-generated. Do not edit!

// (in-package dobot.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class TransPuzzleCmdRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.src_x = null;
      this.src_y = null;
      this.dst_x = null;
      this.dst_y = null;
    }
    else {
      if (initObj.hasOwnProperty('src_x')) {
        this.src_x = initObj.src_x
      }
      else {
        this.src_x = 0.0;
      }
      if (initObj.hasOwnProperty('src_y')) {
        this.src_y = initObj.src_y
      }
      else {
        this.src_y = 0.0;
      }
      if (initObj.hasOwnProperty('dst_x')) {
        this.dst_x = initObj.dst_x
      }
      else {
        this.dst_x = 0.0;
      }
      if (initObj.hasOwnProperty('dst_y')) {
        this.dst_y = initObj.dst_y
      }
      else {
        this.dst_y = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type TransPuzzleCmdRequest
    // Serialize message field [src_x]
    bufferOffset = _serializer.float32(obj.src_x, buffer, bufferOffset);
    // Serialize message field [src_y]
    bufferOffset = _serializer.float32(obj.src_y, buffer, bufferOffset);
    // Serialize message field [dst_x]
    bufferOffset = _serializer.float32(obj.dst_x, buffer, bufferOffset);
    // Serialize message field [dst_y]
    bufferOffset = _serializer.float32(obj.dst_y, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type TransPuzzleCmdRequest
    let len;
    let data = new TransPuzzleCmdRequest(null);
    // Deserialize message field [src_x]
    data.src_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [src_y]
    data.src_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [dst_x]
    data.dst_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [dst_y]
    data.dst_y = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 16;
  }

  static datatype() {
    // Returns string type for a service object
    return 'dobot/TransPuzzleCmdRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0f3206cd72d7e1677e9cd0b316eda50b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 src_x
    float32 src_y
    float32 dst_x
    float32 dst_y
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new TransPuzzleCmdRequest(null);
    if (msg.src_x !== undefined) {
      resolved.src_x = msg.src_x;
    }
    else {
      resolved.src_x = 0.0
    }

    if (msg.src_y !== undefined) {
      resolved.src_y = msg.src_y;
    }
    else {
      resolved.src_y = 0.0
    }

    if (msg.dst_x !== undefined) {
      resolved.dst_x = msg.dst_x;
    }
    else {
      resolved.dst_x = 0.0
    }

    if (msg.dst_y !== undefined) {
      resolved.dst_y = msg.dst_y;
    }
    else {
      resolved.dst_y = 0.0
    }

    return resolved;
    }
};

class TransPuzzleCmdResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.result = null;
    }
    else {
      if (initObj.hasOwnProperty('result')) {
        this.result = initObj.result
      }
      else {
        this.result = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type TransPuzzleCmdResponse
    // Serialize message field [result]
    bufferOffset = _serializer.int32(obj.result, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type TransPuzzleCmdResponse
    let len;
    let data = new TransPuzzleCmdResponse(null);
    // Deserialize message field [result]
    data.result = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'dobot/TransPuzzleCmdResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '034a8e20d6a306665e3a5b340fab3f09';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 result
    
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new TransPuzzleCmdResponse(null);
    if (msg.result !== undefined) {
      resolved.result = msg.result;
    }
    else {
      resolved.result = 0
    }

    return resolved;
    }
};

module.exports = {
  Request: TransPuzzleCmdRequest,
  Response: TransPuzzleCmdResponse,
  md5sum() { return '80257a33fbe8eda7e69a8ee2a7a08d79'; },
  datatype() { return 'dobot/TransPuzzleCmd'; }
};
