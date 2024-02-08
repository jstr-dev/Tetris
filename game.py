from graphics import Graphics
from block import * 
import random 
import pygame
import time 

# Direction offset
DIRECTION_OFFSET = {
    pygame.K_RIGHT: 1,
    pygame.K_LEFT: -1
}

SPEED_KEY = pygame.K_DOWN
ROTATE_RIGHT_KEY = pygame.K_UP 
ROTATE_LEFT_KEY = pygame.K_z
HOLD_BLOCK_KEY = pygame.K_c
HARD_DROP_BLOCK_KEY = pygame.K_SPACE

class Game():
    def __init__(self):
        """Set up initial values"""

        # Pygame
        pygame.init()
        pygame.display.set_caption("Tetris :)")

        # Graphics
        self.graphics = Graphics((640+190, 850), self)
        self.graphics.setDrawLines(False)

        # Logic info 
        self.running = False

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

        # Holding block info
        self.holding = None 
        self.has_triggered_holding = False

        # Initially add first block to grid
        self.chooseNextBlock()

    def chooseNextBlock(self): 
        """Chooses the next block and appends a new one"""
        self.current_block = self.next_blocks.pop(0)
        self.next_blocks.append(random.choice(BLOCKS)(self))
        self.current_block.addToGrid()

    def holdCurrentBlock(self):
        """Holds the current block and replaces the current block with either a new block, or what was in holding prior"""
        # If they have already tried to hold a block this turn, we disallow it.
        if (self.has_triggered_holding): return 
        
        # Store the current block in a temp variable and remove it from the grid
        self.current_block.removeFromGrid()
        temp_block = self.current_block 

        if (self.holding != None):
            self.current_block = self.holding
            self.current_block.resetPosition()
            self.current_block.addToGrid() 
        else:
            self.chooseNextBlock()

        self.holding = temp_block 
        self.has_triggered_holding = True 

    def tick(self):
        """Called every tick"""
        self.blockLogic()

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
        if key == ROTATE_RIGHT_KEY:
            self.current_block.rotate(90)
        if key == ROTATE_LEFT_KEY:
            self.current_block.rotate(-90)
        if key == HOLD_BLOCK_KEY:
            self.holdCurrentBlock()
        if key == HARD_DROP_BLOCK_KEY:
            self.current_block.drop()

    def registerKeyRelease(self, key):
        """Key listener"""
        if key == SPEED_KEY:
            self.block_time = 0.5

    def blockLogic(self):
        self.checkClearLines()
        time_since_drop = time.time() - self.last_drop
        if time_since_drop > self.block_time:
            self.last_drop = time.time()
            # Collision detection
            collision = self.current_block.willCollideWithBlock(0, 1)
            if collision:
                self.chooseNextBlock()
                self.has_triggered_holding = False 
            else:
                self.current_block.moveDown()

    def checkClearLines(self):
        """Check and clear any completed lines from the grid"""
        lines_to_clear = []
        for y in range(self.height):
            if all(cell != 0 for cell in self.grid[y]):
                lines_to_clear.append(y)

        for y in lines_to_clear:
            # Clear the line by setting all cells to 0
            for x in range(self.width):
                self.grid[y][x] = 0
                self.gridcol[y][x] = None 

            # Move all lines above the cleared line down by 1
            for row in range(y, 0, -1):
                self.grid[row] = self.grid[row - 1]
                self.gridcol[row] = self.gridcol[row - 1]

            # Insert a new empty line at the top
            self.grid[0] = [0] * self.width
            self.gridcol[0] = [None] * self.width

    def start(self):
        self.running = True 

        while self.running:
           self.tick()

    def quit(self):
        self.running = False 
        pygame.quit()