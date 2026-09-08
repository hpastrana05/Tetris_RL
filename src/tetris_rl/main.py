import random

import pygame
from tetris_rl.config import *
pygame.init()

def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

def draw_side_panel(screen):
    panel_x = NUM_COLS * BLOCK_SIZE
    pygame.draw.rect(screen, GRAY, (panel_x, 0, WINDOW_WIDTH - panel_x, WINDOW_HEIGHT))
    
def draw_piece(screen, piece, position):
    shape, color = piece
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, 
                                 color, 
                                 (position[0] * BLOCK_SIZE + x * BLOCK_SIZE, 
                                  position[1] * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    # Set up the game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris RL")

    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state here
        actual_piece = SHAPES[random.randint(0, len(SHAPES) - 1)]  # Randomly select a piece for demonstration

        # Clear the screen
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_side_panel(screen)
        draw_piece(screen, actual_piece, (NUM_COLS // 2, 0))  # Draw the actual piece at the top center
        


        # Draw game elements here
        
        
        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()