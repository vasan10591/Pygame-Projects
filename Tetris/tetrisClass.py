import pygame, random, copy

class Shape:
    def __init__(self, listLoc, anchorIndex, color):
        self.listLoc = listLoc
        self.anchorIndex = anchorIndex
        self.x = None
        self.y = None
        self.color = color

    def sampleRot(self):
        return [(-p[1],p[0]) for p in self.listLoc]
    
class Node:
    def __init__(self, occupied = 0, color = None):
        self.occupied = occupied
        self.color = color

# Box size 30
class Window:
    xS = 450
    yS = 600
    bSize = 30
    shapeList = [Shape([(0,-2),(0,-1),(0,0),(0,1),(0,2)], 2,(0,191,255)), \
            Shape([(0,-1),(0,0),(0,1),(-1,1)],1,(0,0,255)), \
            Shape([(0,-1),(0,0),(0,1),(1,1)],1,(255,165,0)), \
            Shape([(0,0),(1,0),(0,1),(1,1)], None, (255,255,0)), \
            Shape([(1,-1),(0,-1),(0,0),(-1,0)],2,(124,252,0)), \
            Shape([(0,-1),(0,0),(1,0),(-1,0)],1,(186,85,211)), \
            Shape([(-1,-1),(0,-1),(0,0),(1,0)],2,(255,0,0))]
    rectTp = pygame.Surface((27, 27))
    def __init__(self, xL, yL, screen, highestRow = -1):
        self.screen = screen
        self.xL = xL
        self.yL = yL
        self.disTiles = [[Node()]*20 for _ in range(15)]
        for i in range(len(self.disTiles)):
            self.disTiles[i].append(Node(occupied = 2))
        self.currTile = None
        self.highestRow = highestRow
        self.setup()
        self.resetCurrTile()
        self.frameUpdate()
        self.over = False
        self.currHeld = None
        self.shiftPress = False
            
    def setup(self):
        self.screen.fill((0,0,0))
        # Border
        pygame.draw.rect(self.screen, (192,192,192), pygame.Rect(self.xL-6, self.yL-6, Window.xS+12, Window.yS+12)) 
        # Display
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(self.xL, self.yL, Window.xS, Window.yS))
        for i in range(20):
            if(i<15):
                pygame.draw.line(self.screen, (15,15,15), (self.xL+(i*Window.bSize), self.yL), (self.xL+(i*Window.bSize), self.yL + Window.yS))
            pygame.draw.line(self.screen, (15,15,15), (self.xL, self.yL+(i*Window.bSize)),(self.xL + Window.xS, self.yL+(i*Window.bSize))) 
    
    def frameUpdate(self):
        # If there is a space below
        if(self.spaceBelow()):
            self.currTile.y += 1
            self.disTilesUpdate()
            self.disTilesDraw()
            self.drawBottom()
        else:
            for p in self.currTile.listLoc:
                self.disTiles[self.currTile.x + p[0]][self.currTile.y + p[1]].occupied = 2
            self.updateRowClear()
            self.shiftPress = False
            result = self.resetCurrTile()
            if not result:
                self.over = True
            else: self.frameUpdate()
    
    def hold(self):
        if(not self.shiftPress):
            if (self.currHeld != None):
                plc = self.currHeld
                self.currHeld = self.currTile
                self.resetCurrTile(plc)
            else:
                self.currHeld = self.currTile
                self.resetCurrTile()
            self.shiftPress = True
            self.frameUpdate()

    def drawBottom(self):
        img = [copy.copy(Window.rectTp)] * len(self.currTile.listLoc)
        for x in img:
            x.set_colorkey((0,0,0))
            x.set_alpha(50)
        y = self.currTile.y
        while(self.spaceBelow(y)):
            y+=1
        for i,p in enumerate(self.currTile.listLoc):
            pygame.draw.rect(img[i],self.currTile.color,img[i].get_rect())
            self.screen.blit(img[i], (self.xL +(Window.bSize*(self.currTile.x + p[0])), self.yL + (Window.bSize*(y + p[1]))))

    def moveDown(self):
        if(self.spaceBelow()):
            self.currTile.y +=1
            self.disTilesUpdate()
            self.disTilesDraw()
            self.drawBottom()

    def drop(self):
        while(self.spaceBelow()):
            self.currTile.y +=1
            self.disTilesUpdate()
        self.frameUpdate()

    def updateRowClear(self):
        while True:
            restart = False
            for i in range(len(self.disTiles[0]) - 2, 0, -1):
                rowP = [row[i] for row in self.disTiles]
                if(all(elem.occupied == 2 for elem in rowP)):
                    for p in range(i-1, 0, -1):
                        for q in range(len(self.disTiles)):
                            self.disTiles[q][p+1] = self.disTiles[q][p]
                    restart = True
                    break
            if not restart:
                break

    def spaceBelow(self, y = -25):
        if (y == -25): y = self.currTile.y
        for p in self.currTile.listLoc:
            if(self.disTiles[self.currTile.x + p[0]][y + p[1] + 1].occupied == 2):
                return False
        return True

    def resetCurrTile(self, hold = None):
        if (hold == None):
            self.currTile = copy.copy(random.choice(Window.shapeList))
        else: self.currTile = hold
        self.currTile.x = 7
        self.currTile.y = 2 
        index = 0
        for p in self.currTile.listLoc:
            if self.disTiles[self.currTile.x + p[0]][self.currTile.y + p[1]].occupied == 2:
                index = p[1] if p[1] > index else index
        self.currTile.y = self.currTile.y - index
        q = [self.currTile.y + m[1] < 0 for m in self.currTile.listLoc]
        if True in q:
            newListLoc = []
            for k,v in enumerate(q):
                if not v: newListLoc.append(self.currTile.listLoc[k])
            self.currTile.listLoc = newListLoc
            self.disTilesUpdate()
            self.disTilesDraw()
            return False
        return True

    def disTilesDraw(self):
        self.setup()
        for i in range(len(self.disTiles)):
            for j in range(len(self.disTiles[i])):
                if(self.disTiles[i][j].occupied>0 and self.disTiles[i][j].color != None):
                    pygame.draw.rect(self.screen, self.disTiles[i][j].color, pygame.Rect(self.xL+(Window.bSize*i), self.yL+(Window.bSize*j), Window.bSize - 3, Window.bSize - 3))

    def disTilesUpdate(self):
        for i in range(len(self.disTiles)):
            for j in range(len(self.disTiles[i])):
                if (self.disTiles[i][j].occupied == 1):
                    self.disTiles[i][j] = Node()
        for p in self.currTile.listLoc:
            self.disTiles[self.currTile.x + p[0]][self.currTile.y + p[1]] = Node(1,self.currTile.color)
    
    def translate(self,direc,amt = 1):
        canTrans = True
        if(direc == 1):
            for q in self.currTile.listLoc:
                if((self.currTile.x + q[0]) == len(self.disTiles) - 1):
                    canTrans = False
                    break
                elif(self.disTiles[self.currTile.x + q[0] + 1][self.currTile.y + q[1]].occupied == 2):
                    canTrans = False
                    break
                else: pass
        else:
            for y in self.currTile.listLoc:
                if((self.currTile.x + y[0]) == 0):
                    canTrans = False
                    break
                elif(self.disTiles[self.currTile.x + y[0] - 1][self.currTile.y + y[1]].occupied == 2):
                    canTrans = False
                    break
                else: pass
        
        if canTrans:
            self.currTile.x += direc * amt
            self.disTilesUpdate()
            self.disTilesDraw()
            self.drawBottom()
            return True
        else:
            return False
    
    # (h,k) --> (-k, h) 
    def rotate(self):
        canRot = True
        if self.currTile.anchorIndex != None:
            tempListLoc = self.currTile.sampleRot()
            index = 0
            if (self.currTile.x < 4):
                for p in tempListLoc:
                    if(p[0] + self.currTile.x < 0):
                        index = p[0] if (p[0]) < index else index
            elif (self.currTile.x > len(self.disTiles) - 5):
                for q in tempListLoc:
                    if(q[0] + self.currTile.x > len(self.disTiles) - 1):
                        index = q[0] if (q[0]) > index else index
            else: pass
            tempX = self.currTile.x - index
            for rp in tempListLoc:
                if(self.disTiles[tempX+rp[0]][self.currTile.y + rp[1]].occupied == 2):
                    if(index != 0):
                        canRot = False
                        break
                    else:
                        if(self.currTile.x < tempX + rp[0]):
                            index = rp[0] if (rp[0] >= index) else index
                        else:
                            index = rp[0] if (rp[0] < index) else index
            index = -index
            if canRot:
                result = True
                plcH = self.currTile.listLoc
                if (index != 0):
                    self.currTile.listLoc = tempListLoc
                    result = self.translate(int(index/abs(index)),int(abs(index)))
                if result:
                    self.currTile.listLoc = tempListLoc
                    self.disTilesUpdate()
                    self.disTilesDraw()
                    self.drawBottom()
                else:
                    self.currTile.listLoc = plcH
