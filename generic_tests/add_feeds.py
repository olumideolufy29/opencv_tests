# Load two images

import numpy as np
import cv2

cap = cv2.VideoCapture(0)


while(True):
    ret, frame = cap.read()
    rows = frame.shape[0]
    cols = frame.shape[1]

    roi = frame[0:rows, 0:cols]

    roi[0:rows, 0:cols/2] = frame[0:rows, cols/2:cols]

    cv2.imshow('test', roi)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
