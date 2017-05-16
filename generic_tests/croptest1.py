import numpy as np
import cv2

#Below is required for keyboard inputs
import termios, fcntl, sys, os
fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
##Keyboard input init code ends here

cap = cv2.VideoCapture(0)

first_shot = True
x,y = 0,0
old_x, old_y, = 0,0


def readPos(current_x,current_y):
    try:
        while 1:
            c = sys.stdin.read(1)
    
    
            if repr(c) == 's':
                current_y = current_y + 5
                print x,y
            if repr(c) == 'w':
                current_y = current_y - 5
                print x,y
    except IOError: pass
    
    """
    if cv2.waitKey(1) == ord('a'):
        current_x = current_x - 5
    if cv2.waitKey(1) == ord('d'):
        current_x = current_x + 5
    """
    
    return (current_x,current_y)
    

while(True):
    # Capture frame-by-frame.
    ret, frame = cap.read()
    # Our operations on the frame come here.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if (first_shot):
        x, old_x = frame.shape[1]/2.0, frame.shape[1]/2.0
        y, old_y = frame.shape[0]/2.0, frame.shape[0]/2.0

        w = frame.shape[1]
        h = 100.0

        first_shot = False
    
    x,y = readPos(old_x, old_y)
    w = h/480*640
    
    #Crop the feed ([startY:endY, startX:endX] format)
    crop_img = gray[y-h/2:y+h/2, x-w/2:x+w/2]
    
    
    #Resize the feed to a 480 x 640 format
    resized = cv2.resize(crop_img, (640, 480))

    
    # Display the resulting frames.
    cv2.imshow('Black & White Frame', gray)
    cv2.imshow('Cropped', crop_img)
    cv2.imshow('resized', resized)
    
    old_x = x
    old_y = y

    # Quit on holding ESC
    if cv2.waitKey(1) == 27:
        break
        

# When everything done, release the capture.
cap.release()
cv2.destroyAllWindows()
termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
