import pygame

from tetris_rl.tetris_actions import TetrisActions
from tetris_rl.tetris import Tetris
from tetris_rl.piece import Piece
from tetris_rl.config import *

def draw_grid(tetris: Tetris, screen):
    for y, row in enumerate(tetris.board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, GRAY, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            pygame.draw.rect(screen, GRID_COLOR, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_piece(piece: Piece, screen):
    for y, row in enumerate(piece.shape):
        for x, col in enumerate(row):
            if col:
                dx = piece.pos_x + x
                dy = piece.pos_y + y

                pygame.draw.rect(screen, piece.color, (dx*BLOCK_SIZE, dy*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_sideboard(tetris: Tetris, screen):
    pygame.draw.rect(screen, GRID_COLOR, (NUM_COLS*BLOCK_SIZE, 0, SIDE_BOARD_SIZE*BLOCK_SIZE, HEIGHT_SAVED*BLOCK_SIZE))
    
    saved = tetris.saved_piece
    
    if saved:
        x_size_saved = len(saved.shape[0])
        y_size_saved = len(saved.shape)
        for y, row in enumerate(saved.shape):
                for x, col in enumerate(row):
                    if col:
                        
                        dx = HALF_SIDE_BOARD - x_size_saved* BLOCK_SIZE / 2 + x * BLOCK_SIZE

                        dy = HEIGHT_SAVED*BLOCK_SIZE//2 + (y - y_size_saved//2)*BLOCK_SIZE

                        pygame.draw.rect(screen, saved.color, (dx, dy, BLOCK_SIZE, BLOCK_SIZE))

    for i in range(N_SHOWED_PIECES):
        piece = tetris.next_pieces[i]
        x_size = len(piece.shape[0])
        y_size = len(piece.shape)
        for y, row in enumerate(piece.shape):
            for x, col in enumerate(row):
                if col:

                    dx = HALF_SIDE_BOARD - x_size * BLOCK_SIZE / 2 + x * BLOCK_SIZE

                    dy = HEIGHT_SAVED*BLOCK_SIZE + i*BLOCK_SIZE*3 + y*BLOCK_SIZE

                    pygame.draw.rect(screen, piece.color, (dx, dy, BLOCK_SIZE, BLOCK_SIZE))


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

    fall_elapsed = 0
    
    
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key in actions.keys():
                tetris.step(actions[event.key])

        # Update game 
        if running and not tetris.game_over:
            fall_interval = max(MAX_VELOCITY, MIN_VELOCITY * 0.8 ** tetris.level)
            fall_elapsed += dt

            while fall_elapsed >= fall_interval and not tetris.game_over:
                fall_elapsed -= fall_interval
                tetris.step(TetrisActions.MOVE_D)
        # Draw game
        screen.fill(BG_COLOR)

        draw_grid(tetris, screen)
        draw_piece(tetris.actual_piece, screen)
        draw_sideboard(tetris, screen)


        
        # Send screen
        pygame.display.flip()

    pygame.quit()
    
    