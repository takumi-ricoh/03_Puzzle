
"use strict";

let SetHOMECmd = require('./SetHOMECmd.js')
let SetJOGCommonParams = require('./SetJOGCommonParams.js')
let SetPTPJointParams = require('./SetPTPJointParams.js')
let GetEndEffectorParams = require('./GetEndEffectorParams.js')
let SetQueuedCmdClear = require('./SetQueuedCmdClear.js')
let GetJOGJointParams = require('./GetJOGJointParams.js')
let GetIOMultiplexing = require('./GetIOMultiplexing.js')
let GetJOGCoordinateParams = require('./GetJOGCoordinateParams.js')
let SetDeviceName = require('./SetDeviceName.js')
let SetARCCmd = require('./SetARCCmd.js')
let ClearAllAlarmsState = require('./ClearAllAlarmsState.js')
let GetCPCmd = require('./GetCPCmd.js')
let SetEMotor = require('./SetEMotor.js')
let GetIODI = require('./GetIODI.js')
let GetJOGCommonParams = require('./GetJOGCommonParams.js')
let GetAlarmsState = require('./GetAlarmsState.js')
let GetDeviceName = require('./GetDeviceName.js')
let SetJOGCoordinateParams = require('./SetJOGCoordinateParams.js')
let SetPTPCoordinateParams = require('./SetPTPCoordinateParams.js')
let SetQueuedCmdForceStopExec = require('./SetQueuedCmdForceStopExec.js')
let SetQueuedCmdStartExec = require('./SetQueuedCmdStartExec.js')
let GetPTPCommonParams = require('./GetPTPCommonParams.js')
let SetEndEffectorGripper = require('./SetEndEffectorGripper.js')
let SetPTPCmd = require('./SetPTPCmd.js')
let SetHOMEParams = require('./SetHOMEParams.js')
let SetCPCmd = require('./SetCPCmd.js')
let GetIOPWM = require('./GetIOPWM.js')
let GetIOADC = require('./GetIOADC.js')
let SetCPParams = require('./SetCPParams.js')
let SetIOMultiplexing = require('./SetIOMultiplexing.js')
let SetWAITCmd = require('./SetWAITCmd.js')
let TransPuzzleCmd = require('./TransPuzzleCmd.js')
let GetIODO = require('./GetIODO.js')
let SetEndEffectorParams = require('./SetEndEffectorParams.js')
let SetPTPJumpParams = require('./SetPTPJumpParams.js')
let GetEndEffectorLaser = require('./GetEndEffectorLaser.js')
let SetQueuedCmdStopExec = require('./SetQueuedCmdStopExec.js')
let GetPTPCoordinateParams = require('./GetPTPCoordinateParams.js')
let GetHOMEParams = require('./GetHOMEParams.js')
let GetEndEffectorSuctionCup = require('./GetEndEffectorSuctionCup.js')
let GetEndEffectorGripper = require('./GetEndEffectorGripper.js')
let GetDeviceVersion = require('./GetDeviceVersion.js')
let SetJOGJointParams = require('./SetJOGJointParams.js')
let SetTRIGCmd = require('./SetTRIGCmd.js')
let SetIOPWM = require('./SetIOPWM.js')
let GetARCParams = require('./GetARCParams.js')
let GetCPParams = require('./GetCPParams.js')
let GetPTPJointParams = require('./GetPTPJointParams.js')
let GetPose = require('./GetPose.js')
let SetJOGCmd = require('./SetJOGCmd.js')
let SetEndEffectorSuctionCup = require('./SetEndEffectorSuctionCup.js')
let GetDeviceSN = require('./GetDeviceSN.js')
let SetPTPCommonParams = require('./SetPTPCommonParams.js')
let GetPTPJumpParams = require('./GetPTPJumpParams.js')
let SetIODO = require('./SetIODO.js')
let SetARCParams = require('./SetARCParams.js')
let SetEndEffectorLaser = require('./SetEndEffectorLaser.js')
let SetCmdTimeout = require('./SetCmdTimeout.js')

module.exports = {
  SetHOMECmd: SetHOMECmd,
  SetJOGCommonParams: SetJOGCommonParams,
  SetPTPJointParams: SetPTPJointParams,
  GetEndEffectorParams: GetEndEffectorParams,
  SetQueuedCmdClear: SetQueuedCmdClear,
  GetJOGJointParams: GetJOGJointParams,
  GetIOMultiplexing: GetIOMultiplexing,
  GetJOGCoordinateParams: GetJOGCoordinateParams,
  SetDeviceName: SetDeviceName,
  SetARCCmd: SetARCCmd,
  ClearAllAlarmsState: ClearAllAlarmsState,
  GetCPCmd: GetCPCmd,
  SetEMotor: SetEMotor,
  GetIODI: GetIODI,
  GetJOGCommonParams: GetJOGCommonParams,
  GetAlarmsState: GetAlarmsState,
  GetDeviceName: GetDeviceName,
  SetJOGCoordinateParams: SetJOGCoordinateParams,
  SetPTPCoordinateParams: SetPTPCoordinateParams,
  SetQueuedCmdForceStopExec: SetQueuedCmdForceStopExec,
  SetQueuedCmdStartExec: SetQueuedCmdStartExec,
  GetPTPCommonParams: GetPTPCommonParams,
  SetEndEffectorGripper: SetEndEffectorGripper,
  SetPTPCmd: SetPTPCmd,
  SetHOMEParams: SetHOMEParams,
  SetCPCmd: SetCPCmd,
  GetIOPWM: GetIOPWM,
  GetIOADC: GetIOADC,
  SetCPParams: SetCPParams,
  SetIOMultiplexing: SetIOMultiplexing,
  SetWAITCmd: SetWAITCmd,
  TransPuzzleCmd: TransPuzzleCmd,
  GetIODO: GetIODO,
  SetEndEffectorParams: SetEndEffectorParams,
  SetPTPJumpParams: SetPTPJumpParams,
  GetEndEffectorLaser: GetEndEffectorLaser,
  SetQueuedCmdStopExec: SetQueuedCmdStopExec,
  GetPTPCoordinateParams: GetPTPCoordinateParams,
  GetHOMEParams: GetHOMEParams,
  GetEndEffectorSuctionCup: GetEndEffectorSuctionCup,
  GetEndEffectorGripper: GetEndEffectorGripper,
  GetDeviceVersion: GetDeviceVersion,
  SetJOGJointParams: SetJOGJointParams,
  SetTRIGCmd: SetTRIGCmd,
  SetIOPWM: SetIOPWM,
  GetARCParams: GetARCParams,
  GetCPParams: GetCPParams,
  GetPTPJointParams: GetPTPJointParams,
  GetPose: GetPose,
  SetJOGCmd: SetJOGCmd,
  SetEndEffectorSuctionCup: SetEndEffectorSuctionCup,
  GetDeviceSN: GetDeviceSN,
  SetPTPCommonParams: SetPTPCommonParams,
  GetPTPJumpParams: GetPTPJumpParams,
  SetIODO: SetIODO,
  SetARCParams: SetARCParams,
  SetEndEffectorLaser: SetEndEffectorLaser,
  SetCmdTimeout: SetCmdTimeout,
};
