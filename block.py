import random

colours = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255)
]


class Block:
    """Class for tetris blocks"""

    def __init__(self, game):
        self.relative_pos = None
        self.colour = None
        self.width = None
        self.height = None
        self.y = None
        self.x = None
        self.pattern = None
        self.game = game

    def reset_position(self):
        self.x = 5 - (self.width // 2)
        self.y = 0

    def set_pattern(self, pattern):
        """Defines the shape of the block"""
        self.pattern = pattern
        self.pattern = self.get_rotated_pattern(90 * random.randrange(0, 4))

        self.height = len(self.pattern)
        self.width = len(self.pattern[0])
        self.reset_position()

        self.colour = colours[random.randrange(0, 5)]
        self.relative_pos = set()

    def get_colour(self):
        return self.colour

    def is_within_boundaries(self, x, y, pattern=None):
        """Check if the new position is within the game boundaries"""
        height = pattern is not None and len(pattern) or self.height
        width = pattern is not None and len(pattern[0]) or self.width

        return 0 <= y <= self.game.height - height and 0 <= x <= self.game.width - width

    def will_collide_with_block(self, x_offset=0, y_offset=0, pattern=None):
        """Check if the block will collide with another block at the new position"""
        if not self.is_within_boundaries(self.x + x_offset, self.y + y_offset, pattern):
            return True

        for y, row in enumerate(pattern is not None and pattern or self.pattern):
            for x, state in enumerate(row):
                if state == 1:
                    new_y = self.y + y + y_offset
                    new_x = self.x + x + x_offset

                    if self.game.grid[new_y][new_x] != 0 and (new_y, new_x) not in self.relative_pos:
                        return True

        return False

    def add_to_grid(self):
        """Adding the block to game's grid at its current x, y cords"""
        self.relative_pos = set()
        for y, row in enumerate(self.pattern):
            for x, state in enumerate(row):
                if state == 1:
                    self.game.grid[self.y + y][self.x + x] = state
                    self.game.grid_col[self.y + y][self.x + x] = state and self.get_colour() or None
                    self.relative_pos.add((self.y + y, self.x + x))

    def remove_from_grid(self):
        """Remove block from the grid"""
        for y, row in enumerate(self.pattern):
            for x, state in enumerate(row):
                if state == 1:
                    self.game.grid[self.y + y][self.x + x] = 0
                    self.game.grid_col[self.y + y][self.x + x] = None

    def move_side(self, offset):
        """Tries to move the tetris block by some x offset"""
        if self.will_collide_with_block(offset): return False

        self.remove_from_grid()
        self.x += offset
        self.add_to_grid()

    def move_down(self):
        """Moves the tetris block down by 1 square"""
        self.remove_from_grid()
        self.y += 1
        self.add_to_grid()

    def get_rotated_pattern(self, angle):
        """Return the pattern of the Tetris block after rotating by the specified angle"""
        rotations = angle // 90
        rotated_pattern = self.pattern

        for _ in range(rotations % 4):
            rotated_pattern = list(zip(*rotated_pattern[::-1]))

        return rotated_pattern

    def rotate(self, angle):
        """Rotates a shape by a specified angle, in 90 degree intervals"""
        new_pattern = self.get_rotated_pattern(angle)

        if self.will_collide_with_block(0, 0, new_pattern): return

        self.remove_from_grid()
        self.pattern = new_pattern
        self.height = len(self.pattern)
        self.width = len(self.pattern[0])
        self.add_to_grid()

    def drop(self):
        """Drop a block to the bottom"""
        while not self.will_collide_with_block(0, 1):
            self.move_down()

        self.game.block_logic()


class StraightBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.set_pattern([
            [1, 1, 1, 1]
        ])


class CubeBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.set_pattern([
            [1, 1],
            [1, 1]
        ])


class TBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.set_pattern([
            [0, 1, 0],
            [1, 1, 1]
        ])


class LBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.set_pattern([
            [1, 0],
            [1, 0],
            [1, 1]
        ])


class JBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.set_pattern([
            [0, 1],
            [0, 1],
            [1, 1]
        ])


class SBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.set_pattern([
            [0, 1, 1],
            [1, 1, 0]
        ])


class ZBlock(Block):
    def __init__(self, game):
        super().__init__(game)
        self.set_pattern([
            [1, 1, 0],
            [0, 1, 1]
        ])


BLOCKS = [StraightBlock, CubeBlock, LBlock, TBlock, JBlock, SBlock, ZBlock]
