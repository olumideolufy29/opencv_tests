import cv2
import numpy as np


cap = cv2.VideoCapture(0)

# mouse callback function
def mouseCallBack(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.line(frame,(100,100),(400,400),(0,255,0),5)
        print x,y

# Create a black image, a window and bind the function to window
#img = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('image')

cv2.namedWindow('WebcamFeed')
cv2.setMouseCallback('WebcamFeed',mouseCallBack)

while(1):
    ret, frame = cap.read()
 
    cv2.imshow('WebcamFeed', frame)

    #cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('a'):
        print ix,iy

cv2.destroyAllWindows()
