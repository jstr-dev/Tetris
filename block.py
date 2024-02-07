import random 

colours = [
    (255, 0, 0), 
    (0, 255, 0), 
    (0, 0, 255), 
    (255, 255, 0),
    (0, 255, 255) 
]

class Block():
    """Class for tetris blocks"""
    def __init__(self, game):
        self.pattern = None 
        self.game = game

    def resetPosition(self):
        self.x = 5 - (self.width // 2)
        self.y = 0 

    def setPattern(self, pattern):
        """Defines the shape of the block"""
        self.pattern = pattern
        self.pattern = self.getRotatedPattern(90 * random.randrange(0, 4)) # Get a randomly rotated shape each time

        self.height = len(self.pattern)
        self.width = len(self.pattern[0])
        self.resetPosition()

        self.colour = colours[random.randrange(0, 5)]
        self.relative_coords = set()
    
    def getColour(self):
        return self.colour 

    def isWithinBoundaries(self, x, y, pattern = None):
        """Check if the new position is within the game boundaries"""
        height = pattern != None and len(pattern) or self.height 
        width = pattern != None and len(pattern[0]) or self.width 

        return 0 <= y <= self.game.height - height and 0 <= x <= self.game.width - width

    def willCollideWithBlock(self, x_offset = 0, y_offset = 0, pattern = None):
        """Check if the block will collide with another block at the new position"""
        if not self.isWithinBoundaries(self.x + x_offset, self.y + y_offset, pattern):
            return True
        
        for y, row in enumerate(pattern != None and pattern or self.pattern):
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

    def getRotatedPattern(self, angle):
        """Return the pattern of the Tetris block after rotating by the specified angle"""
        rotations = angle // 90
        rotated_pattern = self.pattern

        for _ in range(rotations % 4):
            rotated_pattern = list(zip(*rotated_pattern[::-1]))

        return rotated_pattern

    def rotate(self, angle):
        # Get new rotated matrix
        new_pattern = self.getRotatedPattern(angle)

        # Check for collisions
        if self.willCollideWithBlock(0, 0, new_pattern): return 

        self.removeFromGrid()
        self.pattern = new_pattern
        self.height = len(self.pattern)
        self.width = len(self.pattern[0])
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