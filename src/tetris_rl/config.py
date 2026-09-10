
"""
COLORS
"""
BLACK = (0, 0, 0)
GRAY = (54, 54, 54)
BG_COLOR = (18, 18, 24)
GRID_COLOR = (40, 40, 40)

BLUE = (0, 240, 240)
YELLOW = (240, 240, 0)
PURPLE = (160, 0, 240)
GREEN = (0, 220, 80)
RED = (240, 50, 50)
DARK_BLUE = (40, 90, 240)
ORANGE = (240, 150, 30)

"""
VALUES
"""
BLOCK_SIZE = 30
NUM_ROWS = 20
NUM_COLS = 10
SIDE_BOARD_SIZE = 6
HEIGHT_SAVED = 5

TOTAL_WIDTH = (NUM_COLS + SIDE_BOARD_SIZE) * BLOCK_SIZE 

HALF_SIDE_BOARD = NUM_COLS * BLOCK_SIZE + SIDE_BOARD_SIZE * BLOCK_SIZE // 2

FPS = 60

N_NEXT_PIECES=14
GROUP_SIZE=7
N_SHOWED_PIECES=5

WINDOW_WIDTH = NUM_COLS * BLOCK_SIZE + SIDE_BOARD_SIZE*BLOCK_SIZE
WINDOW_HEIGHT = NUM_ROWS * BLOCK_SIZE

SHAPES = [
      ("I", [
          [0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
      ], BLUE),

      ("O", [
          [1, 1],
          [1, 1],
      ], YELLOW),

      ("T", [
          [0, 1, 0],
          [1, 1, 1],
          [0, 0, 0],
      ], PURPLE),

      ("S", [
          [0, 1, 1],
          [1, 1, 0],
          [0, 0, 0],
      ], GREEN),

      ("Z", [
          [1, 1, 0],
          [0, 1, 1],
          [0, 0, 0],
      ], RED),

      ("J", [
          [1, 0, 0],
          [1, 1, 1],
          [0, 0, 0],
      ], DARK_BLUE),

      ("L", [
          [0, 0, 1],
          [1, 1, 1],
          [0, 0, 0],
      ], ORANGE),
  ]

PIECE_QUEUE_SIZE = 5
