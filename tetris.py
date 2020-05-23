import pygame, time
from tetrisClass import Window

pygame.init()
screen = pygame.display.set_mode((700,700))
screen.fill((0,0,0))
done = False
timeT = time.time()
timeQ = time.time()

gameWindow = Window(125,50,screen)

while not done:
    keys = pygame.key.get_pressed()
    if((time.time() - timeQ) > 0.08):
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            gameWindow.translate(-1 if keys[pygame.K_LEFT] else 1)
        if keys[pygame.K_DOWN]:
            gameWindow.moveDown()
        timeQ = time.time()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            done = True
        if event.type == pygame.KEYDOWN:
            #if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            #    gameWindow.translate(-1 if event.key == pygame.K_LEFT else 1)
            if (event.key == pygame.K_UP):
                gameWindow.rotate()
            #elif (event.key == pygame.K_DOWN):
            #    gameWindow.moveDown()
            elif (event.key == pygame.K_SPACE):
                gameWindow.drop()
            elif (event.key == pygame.K_LSHIFT):
                gameWindow.hold()
    if((time.time() - timeT) > 1):
        gameWindow.frameUpdate()
        timeT = time.time()
    if(gameWindow.over == True):
        gameWindow = Window(125,50,screen)
    pygame.display.flip()
