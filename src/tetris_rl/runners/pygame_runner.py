import pygame

from tetris_rl.tetris_actions import TetrisActions
from tetris_rl.tetris import Tetris
from tetris_rl.config import (
    WINDOW_HEIGHT, 
    WINDOW_WIDTH,
    BG_COLOR,
    FPS,
    GRID_COLOR,
    BLOCK_SIZE
)

def draw_grid(tetris: Tetris, screen):
    for y, row in enumerate(tetris.board):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, GRID_COLOR, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(tetris:Tetris, screen):
    piece = tetris.actual_piece

    for y, row in enumerate(piece.shape):
        for x, col in enumerate(row):
            if col:
                dx = piece.pos_x + x
                dy = piece.pos_y + y

                pygame.draw.rect(screen, piece.color, (dx*BLOCK_SIZE, dy*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            


def run(tetris: Tetris):
    pygame.init()

    actions = {
        pygame.K_LEFT : TetrisActions.MOVE_L,
        pygame.K_RIGHT : TetrisActions.MOVE_R,
        pygame.K_DOWN : TetrisActions.MOVE_D,
        pygame.K_SPACE : TetrisActions.DROP,
        pygame.K_a : TetrisActions.ROTATE_180,
        pygame.K_s : TetrisActions.ROTATE_CCW,
        pygame.K_d : TetrisActions.ROTATE_CW,
        pygame.K_f : TetrisActions.SAVE_PIECE
    }

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris RL")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.K_LEFT:
                tetris.step(actions[event.type])
        # Update game 

        # Draw game
        screen.fill(BG_COLOR)

        draw_grid(tetris, screen)
        draw_piece(tetris, screen)


        clock.tick(FPS)
        # Send screen
        pygame.display.flip()

    pygame.quit()
    
    