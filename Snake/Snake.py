import pygame,random,time 

pygame.init()
screen = pygame.display.set_mode((700,700))
done = False
blue = (0, 128, 255)
sLength = 10
bLength = 5
clock = pygame.time.Clock()

class Node:
    def __init__(self, x, y, linkBack = None):
        self.x = x
        self.y = y
        self.linkBack = linkBack

    def selfDraw(self):
        pygame.draw.rect(screen, blue, pygame.Rect(self.x, self.y, 8, 8))

    def rUpdate(self,n):
        temp = (self.x, self.y)
        self.x = n[0]
        self.y = n[1]
        self.selfDraw()
        if self.linkBack is not None: self.linkBack.rUpdate(temp)

class SpecNode(Node):
    def __init__(self, x, y, linkBack, speed, direction):
        super().__init__(x, y, linkBack)
        self.speed = speed
        self.direction = direction

    def update(self):
        self.x += self.speed[0] * sLength
        if self.x >= pygame.display.get_surface().get_width() and self.direction == 'R': self.x = 0
        if self.x < 0 and self.direction == 'L': self.x = pygame.display.get_surface().get_width() - sLength
        self.y += self.speed[1] * sLength
        if self.y >= pygame.display.get_surface().get_height() and self.direction == 'D': self.y = 0
        if self.y < 0 and self.direction == 'U': self.y = pygame.display.get_surface().get_height() - sLength
        self.rUpdate((self.x, self.y))

    def turnUpdate(self,key):
        if(key == pygame.K_RIGHT and self.direction != 'L'):
            self.direction = 'R'
            self.speed = (1,0)
        elif(key == pygame.K_LEFT and self.direction != 'R'):
            self.direction = 'L'
            self.speed = (-1,0)
        elif(key == pygame.K_UP and self.direction !='D'):
            self.direction = 'U'
            self.speed = (0,-1)
        elif(key == pygame.K_DOWN and self.direction != 'U'):
            self.direction = 'D'
            self.speed = (0,1)
        else: pass

    def gameOver(self):
        temp = self.linkBack.linkBack
        while (temp is not None):
            if(temp.x == self.x and temp.y == self.y):
                return True
            else:
                temp = temp.linkBack
        return False

"""def gameOver(currN,x,y):
    if (currN.x == x and currN.y == y):
        print (type(currN))
        return True
    elif (currN.linkBack is not None):
        return gameOver(currN.linkBack,x,y)
    else: return False
"""
tailN = Node(0,screen.get_size()[1]/2, None)

def setup(tailN):
    screen.fill((0,0,0))
    temp = tailN
    for _ in range(bLength-1):
        temp = Node(temp.x + sLength, temp.y, temp)
    headN = SpecNode(temp.x + sLength, temp.y, temp, (1,0), 'R')
    food = Node(random.randint(0,(screen.get_size()[0] - sLength)/sLength)*sLength, random.randint(0,(screen.get_size()[1] - sLength)/sLength)*sLength)
    food.selfDraw()
    return (headN, food)
headN,food = setup(tailN)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            headN.turnUpdate(event.key)
           # time.sleep(0.1)
    if(headN.x == food.x and headN.y == food.y): 
        food = Node(random.randint(0,(screen.get_size()[0] - sLength)/sLength)*sLength, random.randint(0,(screen.get_size()[1] - sLength)/sLength)*sLength)
        temp = Node(tailN.x - sLength, tailN.y, None)
        tailN.linkBack = temp
        tailN = temp
    if headN.gameOver(): headN,food = setup(tailN)
    screen.fill((0,0,0))
    headN.update()
    food.selfDraw()
    pygame.display.flip()
    clock.tick(15)
