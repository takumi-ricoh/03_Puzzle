# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 20:10:18 2017

@author: waida
"""

import commands
import rospy
from dobot.srv import SetPTPCmd
asClientSetPTPCmd = rospy.ServiceProxy("/DobotServer/SetPTPCmd",SetPTPCmd)

def move_pose(res):    
    for i in res:
        #commands.getoutput("rosservice call /DobotServer/SetPTPCmd 1 {} {} {} {}".format(i[0],i[1],i[2],i[3]))
        #commands.getoutput("asClientSetPTPCmd (1 {} {} {} {})".format(i[0],i[1],i[2],i[3]))
        asClientSetPTPCmd(1,i[0],i[1],i[2],i[3])

def read_pose(res):
    pose1 = commands.getoutput("rosservice call /DobotServer/GetPose")
    pose2 = pose1.split()

    x=float(pose2[3])
    y=float(pose2[5])
    z=float(pose2[7])
    r=float(pose2[9])
    
    temp = [x,y,z,r]
    res.append(temp)
