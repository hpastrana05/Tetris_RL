# ==================================================
# COLORS: INTERFACE
# ==================================================
BLACK = (0, 0, 0)
GRAY = (54, 54, 54)
BG_COLOR = (18, 18, 24)
GRID_COLOR = (40, 40, 40)

# ==================================================
# COLORS: PIECES
# ==================================================
BLUE = (0, 240, 240)
YELLOW = (240, 240, 0)
PURPLE = (160, 0, 240)
GREEN = (0, 220, 80)
RED = (240, 50, 50)
DARK_BLUE = (40, 90, 240)
ORANGE = (240, 150, 30)

# ==================================================
# BOARD AND SIDE PANEL
# ==================================================
BLOCK_SIZE = 30  # Size of each cell in pixels.
NUM_ROWS = 20
NUM_COLS = 10
SIDE_BOARD_SIZE = 6  # Panel width in cells.
HEIGHT_SAVED = 5  # Hold area height in cells.

# ==================================================
# WINDOW AND RENDERING
# ==================================================
TOTAL_WIDTH = (NUM_COLS + SIDE_BOARD_SIZE) * BLOCK_SIZE
WINDOW_WIDTH = NUM_COLS * BLOCK_SIZE + SIDE_BOARD_SIZE * BLOCK_SIZE
WINDOW_HEIGHT = NUM_ROWS * BLOCK_SIZE

# Horizontal coordinate of the panel center, in pixels from the window's left edge.
HALF_SIDE_BOARD = NUM_COLS * BLOCK_SIZE + SIDE_BOARD_SIZE * BLOCK_SIZE // 2
FPS = 60

# ==================================================
# PIECE QUEUE AND PREVIEW
# ==================================================
GROUP_SIZE = 7
N_NEXT_PIECES = 14
N_SHOWED_PIECES = 5
PIECE_QUEUE_SIZE = 5

# ==================================================
# LEVELS AND GRAVITY
# ==================================================
LINES_PER_LEVEL = 10

# Fall intervals in milliseconds: shorter intervals mean faster falling.
MAX_VELOCITY = 80
MIN_VELOCITY = 500
LOCK_DELAY = 500  # Time in milliseconds before a grounded piece locks.

# ==================================================
# INITIAL SHAPES: (KIND, MATRIX, COLOR)
# Cells containing 1 form the piece; cells containing 0 are empty.
# ==================================================
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
