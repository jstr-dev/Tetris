import random 

# Direction ENUMS
DIRECTION_RIGHT = 0 
DIRECTION_LEFT = 1 
DIRECTION_UP = 2 
DIRECTION_DOWN = 3 

# Move down results
RESULT_NEWBLOCK = 1
RESULT_SUCCESS = 2
RESULT_FAIL = 3 

colours = [
    (255, 0, 0), #red
    (0, 255, 0), #green
    (0, 0, 255), #blue
    (255, 255, 0), #iforgot 
    (0, 255, 255) # one is cyan one is yellow i think
]

class Block():
    """Class for tetris blocks"""
    def __init__(self, game):
        self.pattern = None 
        self.game = game

    def setPattern(self, pattern):
        """Defines the shape of the block"""
        self.pattern = pattern
        self.direction = random.randrange(0, 3)
        self.height = len(self.pattern)
        self.width = len(self.pattern[0])
        self.x = 5 - (self.width // 2)
        self.y = 0 
        self.colour = colours[random.randrange(0, 4)]
        self.relative_coords = set()
    
    def getColour(self):
        return self.colour 

    def isWithinBoundaries(self, x, y):
        """Check if the new position is within the game boundaries"""
        return 0 <= y <= self.game.height - self.height and 0 <= x <= self.game.width - self.width

    def willCollideWithBlock(self, x_offset = 0, y_offset = 0):
        """Check if the block will collide with another block at the new position"""
        if not self.isWithinBoundaries(self.x + x_offset, self.y + y_offset):
            return True
        
        for y, row in enumerate(self.pattern):
            for x, state in enumerate(row):
                if state == 1:
                    new_y = self.y + y + y_offset
                    new_x = self.x + x + x_offset

                    if self.game.grid[new_y][new_x] != 0 and (new_y, new_x) not in self.relative_coords:
                        return True
        return False

    def addToGrid(self):
        """Adding the block to game's grid at it's current x, y coords"""
        self.relative_coords = set()
        for y, row in enumerate(self.pattern):
            for x, state in enumerate(row):
                if state == 1:
                    self.game.grid[self.y + y][self.x + x] = state
                    self.game.gridcol[self.y + y][self.x + x] = state and self.getColour() or None 
                    self.relative_coords.add((self.y + y, self.x + x))
    
    def removeFromGrid(self):
        """Remove block from the grid"""
        for y, row in enumerate(self.pattern):
            for x, state in enumerate(row):
                if state == 1:
                    self.game.grid[self.y + y][self.x + x] = 0
                    self.game.gridcol[self.y + y][self.x + x] = None 

    def moveSide(self, offset):
        """Tries to move the tetris block by some x offset"""
        # If moving to the left/right will collide then we don't move
        if self.willCollideWithBlock(offset): return False

        # Redraw the shape at the new position
        self.removeFromGrid()
        self.x += offset
        self.addToGrid()
    
    def moveDown(self):
        """Moves the tetris block down by 1 square"""
        # Redraw the shape at the new position
        self.removeFromGrid()
        self.y += 1
        self.addToGrid()

class StraightBlock(Block):
    def __init__(self, game):
       super().__init__(game)
       self.setPattern([
           [1, 1, 1, 1]
       ]) 

class CubeBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.setPattern([
            [1, 1],
            [1, 1]
        ])

class TBlock(Block):
     def __init__(self, game):
        super().__init__(game)
        self.setPattern([
            [0, 1, 0],
            [1, 1, 1]
        ])

class LBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.setPattern([
            [1, 0],
            [1, 0],
            [1, 1]
        ])

class JBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.setPattern([
            [0, 1],
            [0, 1],
            [1, 1]
        ])

class SBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.setPattern([
            [0, 1, 1],
            [1, 1, 0]
        ])

class ZBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.setPattern([
            [1, 1, 0],
            [0, 1, 1]
        ])

BLOCKS = [StraightBlock, CubeBlock, LBlock, TBlock, JBlock, SBlock, ZBlock]
# BLOCKS = [StraightBlock, ZBlock]
# BLOCKS = [ZBlock, SBlock]