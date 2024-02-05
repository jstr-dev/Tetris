import pygame 
import time 

COLOUR_BLACK = (0, 0, 0)

class Graphics():
    def __init__(self, res, game):
        self.width = res[0]
        self.height = res[1]
        self.game = game 

        self.cubeSize = 35

        self.holdX = 50 
        self.holdY = 100
        self.holdWide = self.cubeSize*4
        self.holdTall = self.cubeSize*4

        self.gridWide = 350 
        self.gridTall = self.gridWide * 2
        self.gridX = self.holdX + self.holdWide + 50 
        self.gridY = 100

        self.nextX = self.gridWide + self.gridX + 50 
        self.nextY = 100
        self.nextWide = self.cubeSize*4
        self.nextTall = self.cubeSize*8

        self.graphics = pygame.display.set_mode(res)

        self.running = False 
        self.bgcolor = None 
        self.linecol = None
        self.seccolor = None 

    def render(self):
        self.graphics.fill(self.bgcolor)
        pygame.draw.rect(self.graphics, self.seccolor, (self.gridX, self.gridY, self.gridWide, self.gridTall))

        # draw them thicc blocks 
        for y, d in enumerate(self.game.grid): 
            for x, matrixVal in enumerate(d):
                if matrixVal == 1:
                    pygame.draw.rect(self.graphics, self.game.gridcol[y][x], (self.gridX + (self.cubeSize*x), self.gridY + (self.cubeSize*y), self.cubeSize, self.cubeSize))

        
        # draw board 
        for x in range(11):
            pygame.draw.line(self.graphics, self.linecol, (self.gridX + (self.cubeSize * x), self.gridY), (self.gridX + (self.cubeSize * x), self.gridTall+self.gridY))
        for y in range(21):
            pygame.draw.line(self.graphics, self.linecol, (self.gridX, self.gridY + (self.cubeSize * y)), (self.gridWide + self.gridX, self.gridY + (self.cubeSize * y)))

        # draw next 
        pygame.draw.rect(self.graphics, self.seccolor, (self.nextX, self.nextY, self.nextWide, self.nextTall))
        
        for x in range(5):
            pygame.draw.line(self.graphics, self.linecol, (self.nextX + (self.cubeSize * x), self.nextY), (self.nextX + (self.cubeSize * x), self.nextTall+self.nextY))
        for y in range(9):
            pygame.draw.line(self.graphics, self.linecol, (self.nextX, self.nextY + (self.cubeSize * y)), (self.nextWide + self.nextX, self.nextY + (self.cubeSize * y)))

        # draw hold 
        pygame.draw.rect(self.graphics, self.seccolor, (self.holdX, self.holdY, self.holdWide, self.holdTall))
        
        for x in range(5):
            pygame.draw.line(self.graphics, self.linecol, (self.holdX + (self.cubeSize * x), self.holdY), (self.holdX + (self.cubeSize * x), self.holdTall+self.holdY))
        for y in range(5):
            pygame.draw.line(self.graphics, self.linecol, (self.holdX, self.holdY + (self.cubeSize * y)), (self.holdWide + self.holdX, self.holdY + (self.cubeSize * y)))
        
        pygame.display.update()