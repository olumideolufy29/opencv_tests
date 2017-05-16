#!/usr/bin/env python

#from __future__ import print_function
import roslib
import sys
import rospy
import cv2
#from stdmsgs.msg import String
from sensor_msgs.msg import Image
from marker_detection.msg import MarkerDetectMsg
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import time

x_co = 0
y_co = 0
x = 1
y = 1
w = 1
h = 1
minArea = 200
itemDetected = False

camFOV = 90 #Field of View angle in degrees
feedWidth = 640 #Default feed width

lower_bound = np.array([0,0,0])
upper_bound = np.array([255,255,255])

mes = MarkerDetectMsg()
mes.currentArea = 1
mes.angle = 1

#Initialize node and opencv bridge
rospy.init_node("marker_angle", anonymous=False)
detection = rospy.Publisher("marker_detection", MarkerDetectMsg, queue_size=1)
bridge = CvBridge()

#Node callback
def callback(data):
    try:
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
        
    #Capture frame field width
    feeddWidth = np.size(frame, 1)
    
    #Apply filters for increased detection
    blur = cv2.blur(frame,(5,5))
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    #Target value of target color (H,S,V format). Enter decimal values.
    s = [28.0,77.0,40.0]
    
    #Update lower and upper bounds for further filtering
    #Hue should only be allowed small variations 
    lower_bound = np.array([s[0]-5,s[1]-20,s[2]-50])
    upper_bound = np.array([s[0]+5,s[1]+20,s[2]+50])
    
    #Capture whatever between lower and upper bounds range (black & white).
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    #Get rid of background noise using erosion and fill in the holes using dilation
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    mask = cv2.erode(mask,element, iterations=2)
    mask = cv2.dilate(mask,element,iterations=8)
    
    
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    
    for contour in contours:
        mes.currentArea = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)

        #Compare position with the current display to avoid jumps
        if bestContour is not None:
            x_base, y_base, w_base, h_base = cv2.boundingRect(bestContour) 

        #add if condition
        if mes.currentArea > maximumArea:
            bestContour = contour
            maximumArea = mes.currentArea
            
        #Create a bounding box around the biggest object in color range
    if bestContour is not None:
        
        if mes.currentArea > minArea:
            itemDetected = True
        
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'Position (%d,%d)' %(x,y),(10,50), font, 1,(255,255,255),2)
    
    if itemDetected:
        centerX = x+w/2
        mes.angle = (centerX - feedWidth/2.0)/(feedWidth/2.0)*(camFOV/2.0)
        itemDetected = False
    else:
        mes.currentArea = 0
    
    try:
        detection.publish(mes)
    except CvBridgeError as e:
        print(e)

if __name__ == '__main__':
    topic = rospy.get_param("~topic")
    data = rospy.Subscriber(topic, Image, callback, queue_size=1)


