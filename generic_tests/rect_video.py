import cv2

rect = (0,0,1,1)
rectangle = False
rect_over = False  
def onmouse(event,x,y,flags,params):
    global sceneImg,rectangle,rect,ix,iy,rect_over, roi

    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
#            cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)
            rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))

    elif event == cv2.EVENT_LBUTTONUP:
        rectangle = False
        rect_over = True

        sceneCopy = sceneImg.copy()
        cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)

        rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))       
        roi = sceneImg[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

        cv2.imshow('mouse input', sceneCopy)
        cv2.imwrite('roi.jpg', roi)

# Named window and mouse callback
cv2.namedWindow('mouse input')
cv2.setMouseCallback('mouse input',onmouse)
cv2.namedWindow('video')

camObj = cv2.VideoCapture(-1)
keyPressed = None
running = True
scene = False
# Start video stream
while running:
    readOK, frame = camObj.read()

    keyPressed = cv2.waitKey(5)
    if keyPressed == ord('s'):
        scene = True
        cv2.destroyWindow('video')

        cv2.imwrite('sceneImg.jpg',frame)
        sceneImg = cv2.imread('sceneImg.jpg')

        cv2.imshow('mouse input', sceneImg)

    elif keyPressed == ord('r'):
        scene = False
        cv2.destroyWindow('mouse input')

    elif keyPressed == ord('q'):
        running = False

    if not scene:
        cv2.imshow('video', frame)

cv2.destroyAllWindows()
camObj.release()
