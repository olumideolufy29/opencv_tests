# Retrieved from
# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_depthmap/py_depthmap.html

import numpy as np
import cv2
from matplotlib import pyplot as plt

#imgL = cv2.imread('try2_left.jpg',0)
#imgR = cv2.imread('try2_right.jpg',0)

#imgL = cv2.resize(imgL, (0,0), fx=0.3, fy=0.3)
#imgR = cv2.resize(imgR, (0,0), fx=0.3, fy=0.3)

img = cv2.imread('mars1.jpg',0)

imgL = img[:,0:910]
imgR = img[:,1840-910:1840]


stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)

plt.imshow(disparity,'gray')
plt.show()
