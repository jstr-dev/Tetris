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

DEFAULT_BLOCK_SPEED = 1 
FAST_BLOCK_SPEED = 0.1

class Game:
    def __init__(self):
        """Set up initial values"""

        # Pygame
        pygame.init()
        pygame.display.set_caption("Tetris :)")

        # Graphics
        self.graphics = Graphics((640 + 190, 850), self)
        self.graphics.set_draw_lines(True)

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

        # Fast Mode
        self.fast_mode = False
        self.direction_fast_at = 0

        # Holding block info
        self.holding = None
        self.has_triggered_holding = False

        self.keys = set()
        self.key_duration = dict()
        self.score = 0;
        self.lines = 0

        self.debug_mode = 1
        self.debug_messages = []

        # Drop state, should change each drop 
        self.drop_state = {}
        
        self.show_block_preview = True

    def log(self, message):
        print(f"[DEBUG] [TS: {time.time()}] {message}")

        if self.debug_mode == 0:
            return

        if len(self.debug_messages) > 5:
            self.debug_messages.pop(0)

        self.debug_messages.append(message)

    def get_level(self):
        """Returns the level of the game"""
        return 1 + int(self.lines / 10)

    def on_lines_cleared(self, lines_cleared):
        """Called when lines are cleared"""
        self.score += 100 * self.get_level() * lines_cleared

    def choose_next_block(self):
        """Chooses the next block and appends a new one"""
        self.log("Block changed")
        self.current_block = self.next_blocks.pop(0)
        self.next_blocks.append(random.choice(BLOCKS)(self))
        self.current_block.add_to_grid()

    def get_block_speed(self):
        """Returns the current block speed"""
        if (self.fast_mode):
            return 0.1
        return DEFAULT_BLOCK_SPEED - ((self.get_level() - 1) * 0.05)

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
            bypassDurationOffset = 130000000
            bypassDuration = (self.direction_fast_at != 0 
                              and time.time_ns() > self.direction_fast_at
                              and DIRECTION_OFFSET.get(key)
                              and time.time_ns() > (duration - bypassDurationOffset))
            if duration < time.time_ns() or bypassDuration:
                self.register_key_press(key)
                self.key_duration[key] = time.time_ns() + 200000000

        self.graphics.render()

    def register_key_press(self, key):
        """Key listener"""
        if DIRECTION_OFFSET.get(key):
            self.current_block.move_side(DIRECTION_OFFSET[key])
            if self.direction_fast_at == 0:
                self.direction_fast_at = time.time_ns() + 200000000
        if key == SPEED_KEY:
            self.fast_mode = True 
        if key == ROTATE_RIGHT_KEY:
            self.current_block.rotate(90)
        if key == ROTATE_LEFT_KEY:
            self.current_block.rotate(-90)
        if key == HOLD_BLOCK_KEY:
            self.hold_current_block()
        if key == HARD_DROP_BLOCK_KEY:
            old_y = self.current_block.y
            self.current_block.drop()
            new_y = self.current_block.y
            diff = abs(new_y - old_y)

            if diff:
                self.score += diff * 2

    def register_key_release(self, key):
        """Key listener"""
        if key == SPEED_KEY:
            self.fast_mode = False
        if DIRECTION_OFFSET.get(key):
            self.direction_fast_at = 0

    def force_next_drop(self, offset = 0):
        """Reset the last drop date"""
        if offset > 0:
            self.last_drop = time.time() - offset

        self.last_drop = 0

    def block_logic(self):
        self.check_clear_lines()
        time_since_drop = time.time() - self.last_drop

        if time_since_drop > self.get_block_speed():
            # self.log('Drop')
            self.drop_state = {}
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
                if self.fast_mode:
                    self.score += 1

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
        self.choose_next_block()
        self.running = True

        while self.running:
            self.tick()

    def quit(self):
        self.running = False
        pygame.quit()
