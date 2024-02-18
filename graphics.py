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
        self.bgcolor = (45, 45, 45)
        self.seccolor = (40, 40, 40)
        self.linecol = (230, 230, 230)

        self.draw_lines = True

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

    def render_holding(self):
        pygame.draw.rect(self.graphics, self.seccolor, (self.holdX, self.holdY, self.holdWide, self.holdTall))

        if self.draw_lines:
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
        pygame.draw.rect(self.graphics, self.seccolor, (self.nextX, self.nextY, self.nextWide, self.nextTall))

        if self.draw_lines:
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

    def render(self):
        self.graphics.fill(self.bgcolor)
        pygame.draw.rect(self.graphics, self.seccolor, (self.gridX, self.gridY, self.gridWide, self.gridTall))

        # Render normal game
        self.render_grid()
        self.render_next_blocks()
        self.render_holding()

        pygame.display.update()
