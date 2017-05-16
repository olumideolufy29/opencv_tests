"""
Returns HSV value and coordinate of an area of
a camera feed when double clicked
"""

import cv2
import cv2.cv as cv
import time
import numpy as np

x_co = 0
y_co = 0
mousePressed = False

lowerBound = [0,0,0]
upperBound = [0,0,0]

def on_mouse(event,x,y,flag,param):
    global x_co,y_co,mousePressed
  
    if(event==cv2.EVENT_LBUTTONDBLCLK):
      x_co=x
      y_co=y
      mousePressed = True

#Initialize window and camera
cv2.namedWindow("camera")
capture = cv2.VideoCapture(0)

#Try to get first frame of feed
if capture.isOpened():
    ret, frame = capture.read()
    cv2.setMouseCallback('camera',on_mouse)
else:
    ret = False
    print "Error: can't acquire video frames.\n"

#Runs as long as frames are acquired properly.
while ret:
    blur = cv2.blur(frame,(5,5))
    thr = np.zeros(frame.shape, np.uint8) #Not sure what this line is for
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    s=cv.get2D(hsv,y_co,x_co) #NEED THE cv2 EQUIVALENT!!!, s is an array containing the H-S-V values of the pixel double clicked

    #Display results (mouse position and HSV values)
    if(mousePressed):
        print "Clicked @   X = %r   Y = %r" %(x_co, y_co)
        print "H:",s[0],"      S:",s[1],"       V:",s[2],"\n"
        
        #Update lower and upper bounds for further filtering
        lowerBound = [s[0]-10,s[1]-10,s[2]-10]
        upperBound = [s[0]+10,s[1]+10,s[2]+10]
        
        mousePressed = False
   


    #Show camera feed and update it
    cv2.imshow("camera", frame)
    ret, frame = capture.read()
    
    #Press 'q' to leave program
    if cv2.waitKey(10) == ord('q'):
        break
cv2.destroyAllWindows()

