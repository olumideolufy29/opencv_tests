import numpy as np
import cv2

cap = cv2.VideoCapture(1)

#Set video resolution
#cap.set(3,1280)
#cap.set(4,1024)

while(True):
    # Capture frame-by-frame.
    ret, frame = cap.read()

    # Our operations on the frame come here.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Display the resulting frames.
    cv2.imshow('Normal Frame', frame)
    #cv2.imshow('Alien Frame', hsv)
    #cv2.imshow('Black & White Frame', gray)

    # Quit on 'q'.
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture.
cap.release()
cv2.destroyAllWindows()
