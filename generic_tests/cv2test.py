import cv2
import time
import numpy as np

cv2.namedWindow("Webcam")
vc = cv2.VideoCapture(0)

def onMouse(event,x,y,flag,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print "Hello World!\n"

#if vc.isOpened(): # try to get the first frame
#    rval, frame = vc.read()
#    cv2.setMouseCallback('Webcam',onMouse)
#else:
#    rval = False

rval, frame = vc.read()
cv2.setMouseCallback('Webcam',onMouse)


while rval:
    cv2.imshow("Webcam", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")
