
from tetris_rl.config import BLOCK_SIZE
import pygame


class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.pos_x = 0
        self.pos_y = 0

    def draw(self, screen):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, 
                                     self.color, 
                                     (self.pos_x * BLOCK_SIZE + x * BLOCK_SIZE, 
                                      self.pos_y * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.pos_x + x
                    grid_y = self.pos_y + y
                    if (grid_x < 0 or grid_x >= len(grid[0]) or 
                        grid_y < 0 or grid_y >= len(grid) or 
                        grid[grid_y][grid_x]):
                        return True
        return False

    def move_left(self):
        self.pos_x -= 1

    def move_right(self):
        self.pos_x += 1

    def shift_down(self):
        self.pos_y += 1

    def hard_drop(self, grid):
        while not self.check_collision(grid):
            self.shift_down()
        self.pos_y -= 1  # Move back up one row after collision
        