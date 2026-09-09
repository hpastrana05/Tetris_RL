import random

import pygame
from tetris_rl.config import *
from tetris_rl.piece import Piece

pygame.init()

def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

def set_pos_next_pieces(next_pieces):
    for i in range(min(N_SHOWED_PIECES, len(next_pieces))):
        next_pieces[i].pos_x = NUM_COLS + 1
        next_pieces[i].pos_y = i * 3  + 4 

def draw_side_panel(screen, next_pieces):
    panel_x = NUM_COLS * BLOCK_SIZE
    set_pos_next_pieces(next_pieces)

    pygame.draw.rect(screen, GRAY, (panel_x, 0, WINDOW_WIDTH - panel_x, WINDOW_HEIGHT))
    for i in range(min(N_SHOWED_PIECES, len(next_pieces))):
        next_pieces[i].draw(screen)

def generate_next_pieces(next_pieces):
    next_indexes = list(range(len(SHAPES)))
    random.shuffle(next_indexes)
    if len(next_pieces) in [0, GROUP_SIZE]:
        for i in range(GROUP_SIZE):
            next_pieces.append(Piece(SHAPES[next_indexes[i]][0], SHAPES[next_indexes[i]][1]))



def main():
    # Set up the game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris RL")

    next_pieces = []
    generate_next_pieces(next_pieces)
    saved_piece = Piece([], (0, 0, 0))

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state here
        actual_piece = Piece(SHAPES[0][0], SHAPES[0][1])

        generate_next_pieces(next_pieces)

        # Clear the screen
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_side_panel(screen, next_pieces)
        actual_piece.draw(screen)  # Draw the actual piece at the top center
        


        # Draw game elements here
        
        
        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()