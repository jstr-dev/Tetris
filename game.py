from graphics import Graphics
from block import * 
import random 
import pygame
import time 

DIRECTION_OFFSET = {
    pygame.K_RIGHT: 1,
    pygame.K_LEFT: -1
}

SPEED_KEY = pygame.K_DOWN

class Game():
    def __init__(self):
        """Set up initial values"""

        # Pygame
        pygame.init()
        pygame.display.set_caption("Tetris :)")

        # Graphics
        self.graphics = Graphics((640+190, 850), self)
        self.graphics.bgcolor = (45, 45, 45)
        self.graphics.seccolor = (40, 40, 40)
        self.graphics.linecol = (230, 230, 230)

        # Grid
        self.width = 10 
        self.height = 20 
        self.grid = [[0] * self.width for x in range(self.height)]
        self.gridcol = [[None] * self.width for x in range(self.height)]

        # Block information
        self.current_block = None
        self.next_blocks = [random.choice(BLOCKS)(self) for x in range(3)]
        self.last_drop = time.time()
        self.block_time = 0.5

        # Initially add first block to grid
        self.chooseNextBlock()

    def chooseNextBlock(self): 
        """Chooses the next block and appends a new one"""
        self.current_block = self.next_blocks.pop(0)
        self.next_blocks.append(random.choice(BLOCKS)(self))
        self.current_block.addToGrid()

    def tick(self):
        """Called every tick"""
        time_since_drop = time.time() - self.last_drop
        if time_since_drop > self.block_time:
            self.last_drop = time.time()

            # Collision detection
            collision = self.current_block.willCollideWithBlock(0, 1)
            if collision: 
                self.chooseNextBlock()
            else:
                self.current_block.moveDown()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                return self.quit()
            if e.type == pygame.KEYUP:
                self.registerKeyRelease(e.key)
            if e.type == pygame.KEYDOWN: 
                self.registerKeyPress(e.key) 

        self.graphics.render()

    def registerKeyPress(self, key):
        """Key listener"""
        if DIRECTION_OFFSET.get(key):
            self.current_block.moveSide(DIRECTION_OFFSET[key])
        if key == SPEED_KEY:
            self.block_time = 0.1

    def registerKeyRelease(self, key):
        """Key listener"""
        if key == SPEED_KEY:
            self.block_time = 0.5

    def start(self):
        self.running = True 

        while self.running:
           self.tick()

    def quit(self):
        self.running = False 
        pygame.quit()