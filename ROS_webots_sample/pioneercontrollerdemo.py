#!/usr/bin/env python

import rospy
import time, sys
from std_msgs.msg import String
from webots_ros.srv import *

ctrl = "Pioneer_3_AT_5661_sam"
wheels = ['back_left_wheel', 'back_right_wheel', 'front_left_wheel', 'front_right_wheel']
MAX_SPEED = 6.4
INFINITY = float('inf')

if __name__ == '__main__':
    rospy.init_node('pioneer_controller', anonymous=True)

    print("Using controller: " + ctrl)

    rospy.wait_for_service(ctrl+'/robot/get_device_list')

    try:
        # print device list
        '''deviceLister = rospy.ServiceProxy(ctrl+'/robot/get_device_list', robot_get_device_list)
        dList = deviceLister()
        print("DEVICES:")
        for d in dList.list:
            print(d)'''

        # enable camera
        cameraEnableService = rospy.ServiceProxy(ctrl + '/camera/enable', set_int)
        s = cameraEnableService(1)
        print(s)

        # init motors; position to INFINITY to be able to use velocity
        for wheel in wheels:
            posService = rospy.ServiceProxy(ctrl + '/' + wheel + '/set_position', set_float)
            posService(INFINITY)

        # velociraptors = [1.0, 4.0, 2.0, 6.0]
        velociraptors = [MAX_SPEED, MAX_SPEED, MAX_SPEED, MAX_SPEED] # full speed ahead
        #velociraptors = [-MAX_SPEED, MAX_SPEED, -MAX_SPEED, MAX_SPEED] # turn around mid
        # set velocity
        for (i, wheel) in enumerate(wheels):
            velService = rospy.ServiceProxy(ctrl + '/' + wheel + '/set_velocity', set_float)
            velService(velociraptors[i])

    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

    rospy.spin()
