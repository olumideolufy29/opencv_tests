"""
Returns HSV value and coordinate of an area of
a camera feed when double clicked, and track this color
"""

import cv2
import numpy as np

x_co = 0
y_co = 0
x = 1
y = 1
w = 1
h = 1
currentArea = 1
minArea = 10
itemDetected = False

camFOV = 90 #Field of View angle in degrees
feedWidth = 690

#mousePressed = False

lower_bound = np.array([0,0,0])
upper_bound = np.array([255,255,255])

"""
def on_mouse(event,x,y,flag,param):
    global x_co,y_co,mousePressed
  
    if(event==cv2.EVENT_LBUTTONDBLCLK):
      x_co=x
      y_co=y
      mousePressed = True
"""

#Initialize window and camera
cv2.namedWindow("frame")
capture = cv2.VideoCapture(0)

#Try to get first frame of feed
if capture.isOpened():
    ret, frame = capture.read()
    #cv2.setMouseCallback('frame',on_mouse)

else:
    ret = False
    print "Error: can't acquire video frames.\n"

#Runs as long as frames are acquired properly.
while ret:

    feedWidth = np.size(frame, 1)

    blur = cv2.blur(frame,(5,5))
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #s= cv2.cv.Get2D(cv2.cv.fromarray(hsv),y_co,x_co)
    #print s
    s = [40.0,244.0,179.0]
    #print s
    #Display results (mouse position and HSV values)
    #if(True):
        #print "Clicked @   X = %r   Y = %r" %(x_co, y_co)
        #print "H:",s[0],"      S:",s[1],"       V:",s[2],"\n"
        
        #Update lower and upper bounds for further filtering
        #Hue should only be allowed small variations 
    lower_bound = np.array([s[0]-5,s[1]-20,s[2]-50])
    upper_bound = np.array([s[0]+5,s[1]+20,s[2]+50])

    #Create a binary image, where anything in the color range appears white and everything else is black
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    #Get rid of background noise using erosion and fill in the holes using dilation
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    mask = cv2.erode(mask,element, iterations=2)
    mask = cv2.dilate(mask,element,iterations=8)

    #Create Contours for all the objects within the color range
    #TO DO: Check if biggest cluster of points is around the position of the click
    #TO DO: Check if next cluster is "connected"
    #Maybe improve with contours in the base image

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)

        #Compare position with the current display to avoid jumps
        if bestContour is not None:
            x_base, y_base, w_base, h_base = cv2.boundingRect(bestContour) 

        #add if condition
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
    
    #Create a bounding box around the biggest object in color range
    if bestContour is not None:
        
        if currentArea > minArea:
            itemDetected = True
        
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'Position (%d,%d)' %(x,y),(10,50), font, 1,(255,255,255),2)
    print 'Area: ', currentArea
    
    
    if itemDetected:
        centerX = x+w/2
        print centerX, feedWidth, camFOV
        angle = (centerX - feedWidth/2.0)/(feedWidth/2.0)*(camFOV/2.0)
        print 'Angle: ', angle
        itemDetected = False
    else:
        currentArea = 0
        print 'No marker detected.'


    #Show camera feed and update it
    cv2.imshow("mask",mask)
    cv2.imshow("frame", frame)
    ret, frame = capture.read()

    #Show the contours in a seperate window
    cv2.imshow('mask',mask)
    
    #Press 'q' to leave program
    if cv2.waitKey(10) == ord('q'):
        break
cv2.destroyAllWindows()
