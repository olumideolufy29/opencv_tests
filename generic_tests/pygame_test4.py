from VideoCapture import Device
import pygame
import time
In=1
pygame.init()
w = 640
h = 480
size=(w,h)
screen = pygame.display.set_mode(size) 
c = pygame.time.Clock() # create a clock object for timing

while True:
    cam = Device()
    filename = str(In)+"UI.jpg" # ensure filename is correct
    cam.saveSnapshot(filename) 
    img=pygame.image.load(filename) 
    screen.blit(img,(0,0))
    pygame.display.flip() # update the display
    c.tick(3) # only three images per second
    In += 1
