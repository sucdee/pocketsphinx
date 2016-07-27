#!/usr/bin/env python

"""
voice_cmd_vel.py is a simple demo of speech recognition.
  You can control a mobile base using commands found
  in the corpus file.
"""

import roslib; roslib.load_manifest('pocketsphinx')
import rospy
import math

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import copysign

class voice_cmd_vel:

    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        
        
        # Set a number of parameters affecting the robot's speed
        self.speed = 0.1
        self.max_speed = 0.5        
        self.max_angular_speed = 1.5
        self.angular_speed = 0.5
        self.linear_increment = 0.05
        self.angular_increment = 0.4
        
        # Enable the voice control - initial stage
        self.paused = False
        
        # Initialize the Twist message that we will publish
        self.msg = Twist()

        # Publish to cmd_vel, subscribe to speech output
        self.pub_ = rospy.Publisher('cmd_vel', Twist)
        rospy.Subscriber('recognizer/output', String, self.speechCb)
        
        # We don't want the script to run very fast
        r = rospy.Rate(10.0)
        
        # Ready to receive voice commands -- voice
        
        # Keep pulbishing the cmd_vel message to keep the robot movings
        while not rospy.is_shutdown():
            self.pub_.publish(self.msg)
            r.sleep()
        
    def speechCb(self, msg):
        rospy.loginfo(msg.data)
        
        # If the user has asked to pause/continue voice control, set the flag accordingly
        if msg.data.find("pause speech") > -1:
            self.paused = True
        elif msg.data.find("continue speech") > -1:
            self.paused = False
        
        # If voice control is paused, simply return without performing any action
        if self.paused:
            return  
             

        if msg.data.find("straight") > -1:    
            self.msg.linear.x = self.speed
            self.msg.angular.z = 0

        elif msg.data.find("back") > -1:
            self.msg.linear.x = -self.speed
            self.msg.angular.z = 0
            
        elif msg.data.find("left") > -1:
            if self.msg.linear.x != 0:
                self.msg.angular.z += self.angular_increment
            else:        
                self.msg.angular.z = self.angular_speed
                
        elif msg.data.find("right") > -1:   
            if self.msg.linear.x != 0:
                self.msg.angular.z -= self.angular_increment
            else:        
                self.msg.angular.z = -self.angular_speed
        
        elif msg.data.find("rotate left") > -1:
            self.msg.linear.x = 0
            self.msg.angular.z = self.angular_speed
                
        elif msg.data.find("rotate right") > -1:  
            self.cmd_vel.linear.x = 0      
            self.cmd_vel.angular.z = -self.angular_speed
            
        elif msg.data.find("stop") > -1:          
            self.msg = Twist()

        elif msg.data.find("faster") > -1:
            self.speed += self.linear_increment
            self.angular_speed += self.angular_increment
            if self.msg.linear.x != 0:
                self.msg.linear.x += copysign(self.linear_increment, self.msg.linear.x)
            if self.msg.angular.z != 0:
                self.msg.angular.z += copysign(self.angular_increment, self.msg.angular.z)


        elif msg.data.find("slower") > -1:
            self.speed -= self.linear_increment
            self.angular_speed -= self.angular_increment
            if self.msg.linear.x != 0:
                self.msg.linear.x -= copysign(self.linear_increment, self.msg.linear.x)
            if self.msg.angular.z != 0:
                self.msg.angular.z -= copysign(self.angular_increment, self.msg.angular.z)
                
        
        self.pub_.publish(self.msg)

    def cleanup(self):
        # stop the robot when shutting down!
        twist = Twist()
        self.pub_.publish(twist)

if __name__=="__main__":
    rospy.init_node('voice_cmd_vel')
    try:
        voice_cmd_vel()
    except:
        pass

