
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

WINDOW_WIDTH = NUM_COLS * BLOCK_SIZE + 5*BLOCK_SIZE
WINDOW_HEIGHT = NUM_ROWS * BLOCK_SIZE

SHAPES = [
    ([[1,1,1,1]], BLUE),              # I shape
    ([[1,1], [1,1]], YELLOW),         # O shape
    ([[0,1,0], [1,1,1]], PURPLE),     # T shape
    ([[0,1,1], [1,1,0]], GREEN),      # S shape
    ([[1,1,0], [0,1,1]], RED),        # Z shape
    ([[1,0,0], [1,1,1]], DARK_BLUE),  # J shape
    ([[0,0,1], [1,1,1]], ORANGE)      # L shape
]

PIECE_QUEUE_SIZE = 5
