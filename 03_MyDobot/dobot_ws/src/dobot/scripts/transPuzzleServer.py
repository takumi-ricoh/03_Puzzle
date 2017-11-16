#!/usr/bin/env python
import rospy
import time
import numpy as np
#initialize
from dobot.srv import SetCmdTimeout
from dobot.srv import SetQueuedCmdClear
from dobot.srv import SetQueuedCmdStartExec
from dobot.srv import SetQueuedCmdForceStopExec
from dobot.srv import GetDeviceVersion
from dobot.srv import GetPose
"""HOME : Home Position"""
from dobot.srv import SetHOMEParams
from dobot.srv import SetHOMECmd
"""PTP : point-to-point control"""
from dobot.srv import SetPTPJointParams
from dobot.srv import SetPTPCoordinateParams
from dobot.srv import SetPTPJumpParams
from dobot.srv import SetPTPCommonParams
from dobot.srv import SetPTPCmd
"""CP : continuous-path control"""
from dobot.srv import SetCPParams
from dobot.srv import SetCPCmd
"""EndEffector"""
from dobot.srv import SetEndEffectorParams
from dobot.srv import SetEndEffectorSuctionCup
#Original
from dobot.srv import TransPuzzleCmd

#%%
class TransPuzzle:
    def __init__(self):
        #init instance
        rospy.init_node("TransPuzzleServer")
        self.asClientSetCmdTimeout              = rospy.ServiceProxy("/DobotServer/SetCmdTimeout",SetCmdTimeout)
        self.asClientSetQueuedCmdClear          = rospy.ServiceProxy("/DobotServer/SetQueuedCmdClear",SetQueuedCmdClear)
        self.asClientSetQueuedCmdStartExec      = rospy.ServiceProxy("/DobotServer/SetQueuedCmdStartExec",SetQueuedCmdStartExec)
        self.asClientSetQueuedCmdForceStopExec  = rospy.ServiceProxy("/DobotServer/SetQueuedCmdForceStopExec",SetQueuedCmdForceStopExec)
        self.asClientGetDeviceVersion           = rospy.ServiceProxy("/DobotServer/GetDeviceVersion",GetDeviceVersion)
        self.asClientGetPose                    = rospy.ServiceProxy("/DobotServer/GetPose",GetPose)
        self.asClientSetHOMEParams              = rospy.ServiceProxy("/DobotServer/SetHOMEParams",SetHOMEParams)
        self.asClientSetHOMECmd                 = rospy.ServiceProxy("/DobotServer/SetHOMECmd",SetHOMECmd)
        self.asClientSetEndEffectorParams       = rospy.ServiceProxy("/DobotServer/SetEndEffectorParams",SetEndEffectorParams)
        self.asClientSetPTPJointParams          = rospy.ServiceProxy("/DobotServer/SetPTPJointParams",SetPTPJointParams)        
        self.asClientSetPTPCoordinateParams     = rospy.ServiceProxy("/DobotServer/SetPTPCoordinateParams",SetPTPCoordinateParams)
        self.asClientSetPTPJumpParams           = rospy.ServiceProxy("/DobotServer/SetPTPJumpParams",SetPTPJumpParams)
        self.asClientSetPTPCommonParams         = rospy.ServiceProxy("/DobotServer/SetPTPCommonParams",SetPTPCommonParams)
        self.asClientSetCPParams                = rospy.ServiceProxy("/DobotServer/SetCPParams",SetCPParams)
        self.asClientSetCPCmd                   = rospy.ServiceProxy("/DobotServer/SetCPCmd",SetCPCmd)
        self.asClientSetEndEffectorParams       = rospy.ServiceProxy("/DobotServer/SetEndEffectorParams",SetEndEffectorParams)        
        self.asClientSetPTPCmd                  = rospy.ServiceProxy("/DobotServer/SetPTPCmd",SetPTPCmd)
        self.asClientSetEndEffectorSuctionCup   = rospy.ServiceProxy("/DobotServer/SetEndEffectorSuctionCup",SetEndEffectorSuctionCup)
        
        #init configuraion
        self.func_SetCmdTimeout(3000)
        self.func_SetQueuedCmdClear()
        self.func_SetQueuedCmdStartExec()
        self.func_GetDeviceVersion()
        self.func_SetHOMEParams(200,0,10,0,0) #x, y, z, r,isQueued
        self.func_SetEndEffectorParams(70,0,0,0) #xBias, yBias, zBias,isQueued 
        self.func_SetPTPJointParams([1000,1000,1000,1000],[1000,1000,1000,1000],0) #velocity list, acceleration_list,isQueued 
        self.func_SetPTPCoordinateParams(100,100,100,100,0) #xyzVelocity, xyzAcceleration, rVelocity, rAcceleration,isQueued 
        self.func_SetPTPJumpParams(200,200,0) #jumpHeight, zLimit,isQueued 
        self.func_SetPTPCommonParams(50,50,0) #velocityRatio, accelerationRatio,isQueued 
        
        #home position
        self.func_SetEndEffectorSuctionCup(False)
        #self.func_SetHOMECmd()
        self.func_SetPTPCmd(200,0,-40,0)
        
        #service start
        self.asServerTransPuzzleCmd = rospy.Service("/DobotServer/TransPuzzleCmd",TransPuzzleCmd,self.trans_puzzle_handler)
        rospy.spin()
        
#%%
    """functions"""
    #func1
    def func_SetCmdTimeout(self,timeout):
        self.asClientSetCmdTimeout(timeout)
    
    #func2
    def func_SetQueuedCmdClear(self):
        self.asClientSetQueuedCmdClear()
    
    #func3
    def func_SetQueuedCmdStartExec(self):
        self.asClientSetQueuedCmdStartExec()  
    
    #func4
    def func_GetDeviceVersion(self):
        response = self.asClientGetDeviceVersion()
        print("Device version:%d.%d.%d", response.majorVersion, response.minorVersion, response.revision)
    
    #func
    def func_GetPose(self):
        response = self.asClientGetPose()
        re = [response.x,response.y,response.z,response.r]
        re = np.round(re,2)
        print(re)
        #print("Device version:%d.%d.%d", response.majorVersion, response.minorVersion, response.revision)    
    
    #func
    def func_SetHOMEParams(self, x, y, z, r,isQueued):
        self.asClientSetHOMEParams(x, y, z, r,isQueued)    

    #func
    def func_SetHOMECmd(self):
        self.asClientSetHOMECmd()   
        
    #func
    def func_SetEndEffectorParams(self, xBias, yBias, zBias,isQueued):
        self.asClientSetEndEffectorParams(xBias,yBias,zBias,isQueued)
    
    #func
    def func_SetPTPJointParams(self, velocity_list, acceleration_list,isQueued):
        self.asClientSetPTPJointParams(velocity_list, acceleration_list,isQueued)
    
    #func
    def func_SetPTPCoordinateParams(self, xyzVelocity, xyzAcceleration, rVelocity, rAcceleration,isQueued):
        self.asClientSetPTPCoordinateParams(xyzVelocity,xyzAcceleration,rVelocity,rAcceleration,isQueued)
    
    #func
    def func_SetPTPJumpParams (self, jumpHeight, zLimit,isQueued):
        self.asClientSetPTPJumpParams(jumpHeight, zLimit,isQueued)
    
    #func
    def func_SetPTPCommonParams (self, velocityRatio, accelerationRatio,isQueued):
        self.asClientSetPTPCommonParams(velocityRatio, accelerationRatio,isQueued)

#%%
    """Move function"""
    #PTP function
    def func_SetPTPCmd(self,x,y,z,r):
        ptpMode = 1
        result = self.asClientSetPTPCmd(ptpMode,x,y,z,r).result
        if result != 0: #failed
            rospy.logerr("PTPfailed")
        return result
        
    #Suction function
    def func_SetEndEffectorSuctionCup(self,switch):
        result = self.asClientSetEndEffectorSuctionCup(True,switch,1).result
        return result

#%%
    """callback transpuzzle"""
    #main handler    
    def trans_puzzle_handler(self,req):
        src_x = req.src_x
        src_y = req.src_y
        dst_x = req.dst_x
        dst_y = req.dst_y
        suck_z = -70 #puzzle z

        for i in range(2):
            #1.move src upper	
            res = self.func_SetPTPCmd(src_x,src_y,suck_z+50,0)
            self.func_GetPose()
            #2.suction on
            #res = self.func_SetEndEffectorSuctionCup(True)		
            #3.move src	
            res = self.func_SetPTPCmd(src_x,src_y,suck_z+10,0)
            time.sleep(0.2)
            #4.move src upper	
            res = self.func_SetPTPCmd(src_x,src_y,suck_z+50,0)
            #5.move to dst upper
            res = self.func_SetPTPCmd(dst_x,dst_y,suck_z+50,50)
            #6.move to dst
            res = self.func_SetPTPCmd(dst_x,dst_y,suck_z,50)            
            #7.suction off
            #res = self.func_SetEndEffectorSuctionCup(False)
            time.sleep(0.2)
            #8.move to dst upper (end)
            res = self.func_SetPTPCmd(dst_x,dst_y,suck_z+50,50)
            time.sleep(2)

            #res = self.func_SetEndEffectorSuctionCup(True)		
            res = self.func_SetPTPCmd(dst_x,dst_y,suck_z,50)
            time.sleep(0.3)
            res = self.func_SetPTPCmd(dst_x,dst_y,suck_z+50,50)
            res = self.func_SetPTPCmd(src_x,src_y,suck_z+50,0)
            res = self.func_SetPTPCmd(src_x,src_y,suck_z+10,0)            
            res = self.func_SetEndEffectorSuctionCup(False)
            time.sleep(0.3)
            res = self.func_SetPTPCmd(src_x,src_y,suck_z+50,0) 
            time.sleep(2)  
        
        self.func_SetPTPCmd(200,0,-40,0)        
        
        #return 
        if res==0: #success
            rospy.loginfo("Suck succeeded") 
            result = 0
        else:
            result = 1
        self.bbb = result
        return result

#%%
    """main function"""

if __name__ == "__main__":
    run = TransPuzzle()