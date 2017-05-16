import pygame
pygame.init()
x,y = 0,0
while (True):
    event = pygame.event.get()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            x = x -1
            print x,y
    """
    keys=pygame.key.get_pressed()
    if keys[K_LEFT]:
        x = x - 1
        print x,y
    if keys[K_RIGHT]:
        x = x + 1
        print x,y
    if keys[K_UP]:
        y = y + 1
        print x,y
    if keys[K_DOWN]:
        y = y - 1
        print x,y
    """
    if event.type == QUIT:
        break
pygame.quit()


