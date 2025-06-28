import copy
import pygame

COLOUR_BLACK = (0, 0, 0)


class Graphics:
    def __init__(self, res, game):
        self.width = res[0]
        self.height = res[1]
        self.game = game

        self.cubeSize = 35

        self.holdingSize = 4
        self.holdX = 50
        self.holdY = 100
        self.holdWide = self.cubeSize * self.holdingSize
        self.holdTall = self.cubeSize * self.holdingSize

        self.gridWide = 350
        self.gridTall = self.gridWide * 2
        self.gridX = self.holdX + self.holdWide + 50
        self.gridY = 100

        self.nextX = self.gridWide + self.gridX + 50
        self.nextY = 100
        self.nextWide = self.cubeSize * 4
        self.nextTall = self.cubeSize * 8

        self.graphics = pygame.display.set_mode(res)
        self.primary = (45, 45, 45)
        self.secondary = (40, 40, 40)
        self.linecol = (130, 130, 130)

        self.draw_lines = True
        self.draw_lines_holding = False
        self.draw_lines_next = False

    def set_draw_lines(self, state):
        """Controls whether grid lines should be drawn"""
        self.draw_lines = state

    def render_grid(self):
        for y, d in enumerate(self.game.grid):
            for x, state in enumerate(d):
                if state == 1:
                    pygame.draw.rect(self.graphics, self.game.grid_col[y][x], (
                        self.gridX + (self.cubeSize * x), self.gridY + (self.cubeSize * y), self.cubeSize,
                        self.cubeSize))
                    
        if self.draw_lines:
            for x in range(11):
                pygame.draw.line(self.graphics, self.linecol, (self.gridX + (self.cubeSize * x), self.gridY),
                                 (self.gridX + (self.cubeSize * x), self.gridTall + self.gridY))
            for y in range(21):
                pygame.draw.line(self.graphics, self.linecol, (self.gridX, self.gridY + (self.cubeSize * y)),
                                 (self.gridWide + self.gridX, self.gridY + (self.cubeSize * y)))

        self.render_block_preview()

    def render_holding(self):
        pygame.draw.rect(self.graphics, self.secondary, (self.holdX, self.holdY, self.holdWide, self.holdTall))

        if self.draw_lines_holding:
            for x in range(5):
                pygame.draw.line(self.graphics, self.linecol, (self.holdX + (self.cubeSize * x), self.holdY),
                                 (self.holdX + (self.cubeSize * x), self.holdTall + self.holdY))
            for y in range(5):
                pygame.draw.line(self.graphics, self.linecol, (self.holdX, self.holdY + (self.cubeSize * y)),
                                 (self.holdWide + self.holdX, self.holdY + (self.cubeSize * y)))

        if self.game.holding is not None:
            block = self.game.holding
            hold_x = self.holdX + ((self.cubeSize * self.holdingSize) // 2)
            hold_x = hold_x - ((block.width * self.cubeSize) // 2)
            hold_y = self.holdY + ((self.cubeSize * self.holdingSize) // 2)
            hold_y = hold_y - ((block.height * self.cubeSize) // 2)

            for y, row in enumerate(block.pattern):
                for x, state in enumerate(row):
                    if state == 1:
                        pygame.draw.rect(self.graphics, block.get_colour(), (
                            hold_x + (self.cubeSize * x), hold_y + (self.cubeSize * y), self.cubeSize, self.cubeSize))

    def render_next_blocks(self):
        pygame.draw.rect(self.graphics, self.secondary, (self.nextX, self.nextY, self.nextWide, self.nextTall))

        if self.draw_lines_next:
            for x in range(5):
                pygame.draw.line(self.graphics, self.linecol, (self.nextX + (self.cubeSize * x), self.nextY),
                                 (self.nextX + (self.cubeSize * x), self.nextTall + self.nextY))
            for y in range(9):
                pygame.draw.line(self.graphics, self.linecol, (self.nextX, self.nextY + (self.cubeSize * y)),
                                 (self.nextWide + self.nextX, self.nextY + (self.cubeSize * y)))

        for i in range(len(self.game.next_blocks)):
            # Get the current block
            block = self.game.next_blocks[i]

            if block.height > block.width:
                block.pattern = block.get_rotated_pattern(90)
                block.height = len(block.pattern)
                block.width = len(block.pattern[0])

            # Calculate position
            next_x = self.nextX + ((self.cubeSize * self.holdingSize) // 2)
            next_x -= (block.width * self.cubeSize) // 2
            next_y = self.nextY

            if i > 0:
                next_y += sum(self.game.next_blocks[id].height + 1 for id in range(i)) * self.cubeSize

            for y, row in enumerate(block.pattern):
                for x, state in enumerate(row):
                    if state == 1:
                        pygame.draw.rect(self.graphics, block.get_colour(), (
                            next_x + (self.cubeSize * x), next_y + (self.cubeSize * y), self.cubeSize, self.cubeSize))

    def render_score(self):
        """Render the game score and level"""
        font = pygame.font.SysFont("monospace", 30)
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {self.game.get_level()}", True, (255, 255, 255))
        self.graphics.blit(score_text, (10, 10))
        self.graphics.blit(level_text, (10, 40))

    def render_debug(self):
        font = pygame.font.SysFont("monospace", 15)
        for i, debug in enumerate(self.game.debug_messages):
            text = font.render('DEBUG: ' + debug, True, (255, 255, 255))
            self.graphics.blit(
                text, 
                (self.width - 10 - text.get_width(), self.height - 15 - (15 * i) - 10)
            )

    def render_block_preview(self):
        """Render the block preview, where the block would land if they hard-dropped"""
        block = self.game.current_block

        # Create a deep copy of the block
        shadow_block = type(block)(self.game)
        shadow_block.y = block.y
        shadow_block.x = block.x
        shadow_block.width = block.width
        shadow_block.height = block.height
        shadow_block.relative_pos = copy.deepcopy(block.relative_pos)
        shadow_block.pattern = copy.deepcopy(block.pattern)

        while not shadow_block.will_collide_with_block(0, 1):
            shadow_block.y += 1

        colour = block.get_colour()
        for y, row in enumerate(shadow_block.pattern):
            for x, state in enumerate(row):
                if state == 1:
                    pygame.draw.rect(self.graphics, colour, (
                        self.gridX + (self.cubeSize * (shadow_block.x + x)), 
                        self.gridY + (self.cubeSize * (shadow_block.y + y)), 
                        self.cubeSize, 
                        self.cubeSize), 
                        2
                    )


    def render(self):
        """Renders the game to the screen

        This function clears the screen, renders the main game grid, the next blocks to be spawned, the block that is
        currently being held, the score, and the debug messages. It will then update the display to show the new frame.
        """
        self.graphics.fill(self.primary)
        pygame.draw.rect(self.graphics, self.secondary, (self.gridX, self.gridY, self.gridWide, self.gridTall))

        # Render normal game
        self.render_grid()
        self.render_next_blocks()
        self.render_holding()
        self.render_score()
        self.render_debug()

        pygame.display.update()
