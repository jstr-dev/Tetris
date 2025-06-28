import time

import pygame

from block import *
from graphics import Graphics

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


class Game:
    def __init__(self):
        """Set up initial values"""

        # Pygame
        pygame.init()
        pygame.display.set_caption("Tetris :)")

        # Graphics
        self.graphics = Graphics((640 + 190, 850), self)
        self.graphics.set_draw_lines(False)

        # Logic info
        self.running = False

        # Grid
        self.width = 10
        self.height = 20
        self.grid = [[0] * self.width for _ in range(self.height)]
        self.grid_col = [[None] * self.width for _ in range(self.height)]

        # Block information
        self.current_block = None
        self.next_blocks = [random.choice(BLOCKS)(self) for _ in range(3)]
        self.last_drop = time.time()
        self.block_time = 0.5

        # Holding block info
        self.holding = None
        self.has_triggered_holding = False

        # Initially add first block to grid
        self.choose_next_block()

        self.keys = set()
        self.key_duration = dict()
        self.score = 0;
        self.lines = 0

    def get_level(self):
        """Returns the level of the game"""
        return 1 + int(self.lines / 10)

    def on_lines_cleared(self, lines_cleared):
        """Called when lines are cleared"""
        self.score += 100 * self.get_level() * lines_cleared

    def choose_next_block(self):
        """Chooses the next block and appends a new one"""
        self.current_block = self.next_blocks.pop(0)
        self.next_blocks.append(random.choice(BLOCKS)(self))
        self.current_block.add_to_grid()

    def hold_current_block(self):
        """Holds the current block and replaces the current block with either a new block, or what was in holding
        prior"""
        if self.has_triggered_holding:
            return

        # My comment test
        self.current_block.remove_from_grid()
        temp_block = self.current_block

        if self.holding is not None:
            self.current_block = self.holding
            self.current_block.reset_position()
            self.current_block.add_to_grid()
        else:
            self.choose_next_block()

        self.holding = temp_block
        self.has_triggered_holding = True

    def tick(self):
        """Called every tick"""
        self.block_logic()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return self.quit()
            if e.type == pygame.KEYUP:
                self.keys.remove(e.key)
                self.register_key_release(e.key)
            if e.type == pygame.KEYDOWN:
                self.keys.add(e.key)

        for key in self.keys:
            duration = self.key_duration.get(key, 0)
            if duration < time.time_ns():
                self.register_key_press(key)
                self.key_duration[key] = time.time_ns() + 200000000

        self.graphics.render()

    def register_key_press(self, key):
        """Key listener"""
        if DIRECTION_OFFSET.get(key):
            self.current_block.move_side(DIRECTION_OFFSET[key])
        if key == SPEED_KEY:
            self.block_time = 0.1
        if key == ROTATE_RIGHT_KEY:
            self.current_block.rotate(90)
        if key == ROTATE_LEFT_KEY:
            self.current_block.rotate(-90)
        if key == HOLD_BLOCK_KEY:
            self.hold_current_block()
        if key == HARD_DROP_BLOCK_KEY:
            self.current_block.drop()

    def register_key_release(self, key):
        """Key listener"""
        if key == SPEED_KEY:
            self.block_time = 0.5

    def block_logic(self):
        self.check_clear_lines()
        time_since_drop = time.time() - self.last_drop

        if time_since_drop > self.block_time:
            self.last_drop = time.time()

            # Collision detection
            collision = self.current_block.will_collide_with_block(0, 1)
            if collision:
                self.choose_next_block()
                self.has_triggered_holding = False

                if self.current_block.will_collide_with_block(0, 1):
                    self.running = False
                    print("Game Over")
            else:
                self.current_block.move_down()

    def check_clear_lines(self):
        """Check and clear any completed lines from the grid"""
        lines_to_clear = []
        for y in range(self.height):
            if all(cell != 0 for cell in self.grid[y]):
                lines_to_clear.append(y)

        for y in lines_to_clear:
            # Clear the line by setting all cells to 0
            for x in range(self.width):
                self.grid[y][x] = 0
                self.grid_col[y][x] = None

            # Move all lines above the cleared line down by 1
            for row in range(y, 0, -1):
                self.grid[row] = self.grid[row - 1]
                self.grid_col[row] = self.grid_col[row - 1]

            # Insert a new empty line at the top
            self.grid[0] = [0] * self.width
            self.grid_col[0] = [None] * self.width
            self.lines += 1;

        if len(lines_to_clear) == 0:
            return

        self.on_lines_cleared(len(lines_to_clear))

    def start(self):
        self.running = True

        while self.running:
            self.tick()

    def quit(self):
        self.running = False
        pygame.quit()
