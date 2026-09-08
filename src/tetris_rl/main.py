import random
import pygame
import time

pygame.init()

CELL = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
FPS = 60

BG = (18, 18, 24)
GRID = (48, 48, 62)
WHITE = (235, 235, 235)
SIDE_BG = (24, 24, 32)
GHOST_ALPHA = 80

SHAPES = [
    ([[1, 1, 1, 1]], (0, 240, 240)),
    ([[1, 1], [1, 1]], (240, 240, 0)),
    ([[0, 1, 0], [1, 1, 1]], (160, 0, 240)),
    ([[0, 1, 1], [1, 1, 0]], (0, 220, 80)),
    ([[1, 1, 0], [0, 1, 1]], (240, 50, 50)),
    ([[1, 0, 0], [1, 1, 1]], (40, 90, 240)),
    ([[0, 0, 1], [1, 1, 1]], (240, 150, 30)),
]

PIECE_QUEUE_SIZE = 5


def make_board():
    return [[None for _ in range(COLS)] for _ in range(ROWS)]


def new_piece_from_shape(matrix, color):
    m = [row[:] for row in matrix]
    return {"matrix": m, "color": color, "x": COLS // 2 - len(m[0]) // 2, "y": 0}


def make_bag():
    indices = list(range(len(SHAPES)))
    random.shuffle(indices)
    return indices


def collides(board, piece, dx=0, dy=0, matrix=None):
    matrix = matrix or piece["matrix"]
    for py, row in enumerate(matrix):
        for px, filled in enumerate(row):
            if not filled:
                continue
            x = piece["x"] + px + dx
            y = piece["y"] + py + dy
            if x < 0 or x >= COLS or y >= ROWS:
                return True
            if y >= 0 and board[y][x] is not None:
                return True
    return False


def lock_piece(board, piece):
    for py, row in enumerate(piece["matrix"]):
        for px, filled in enumerate(row):
            if filled:
                x = piece["x"] + px
                y = piece["y"] + py
                if y >= 0:
                    board[y][x] = piece["color"]


def clear_lines(board):
    kept_rows = [row for row in board if any(cell is None for cell in row)]
    cleared = ROWS - len(kept_rows)
    for _ in range(cleared):
        kept_rows.insert(0, [None for _ in range(COLS)])
    return kept_rows, cleared


def rotate_clockwise(matrix):
    return [list(row) for row in zip(*matrix[::-1])]


def rotate_counter_clockwise(matrix):
    return [list(row) for row in zip(*matrix)][::-1]


def rotate_180(matrix):
    return [row[::-1] for row in matrix[::-1]]


def try_rotate_with_wall_kicks(board, piece, direction="cw"):
    if direction == "cw":
        rotated = rotate_clockwise(piece["matrix"])
    elif direction == "ccw":
        rotated = rotate_counter_clockwise(piece["matrix"])
    else:
        rotated = rotate_180(piece["matrix"])

    kicks = [
        (0, 0),
        (-1, 0),
        (1, 0),
        (-2, 0),
        (2, 0),
        (0, -1),
        (-1, -1),
        (1, -1),
    ]

    for dx, dy in kicks:
        if not collides(board, piece, dx=dx, dy=dy, matrix=rotated):
            piece["matrix"] = rotated
            piece["x"] += dx
            piece["y"] += dy
            return True

    return False


def get_ghost_y(board, piece):
    ghost_y = piece["y"]
    while not collides(board, piece, dx=0, dy=ghost_y - piece["y"] + 1):
        ghost_y += 1
    return ghost_y


def draw_cell(surface, x, y, color, cell_size=CELL, alpha=None):
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    if alpha is not None:
        s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        s.fill((*color, alpha))
        surface.blit(s, (x * cell_size, y * cell_size))
        pygame.draw.rect(surface, GRID, rect, 1)
    else:
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, GRID, rect, 1)


def draw_mini_piece(surface, matrix, color, start_x, start_y, cell_size=18):
    for py, row in enumerate(matrix):
        for px, filled in enumerate(row):
            if filled:
                rect = pygame.Rect(
                    start_x + px * cell_size,
                    start_y + py * cell_size,
                    cell_size,
                    cell_size,
                )
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, GRID, rect, 1)


def draw_side_panel(surface, hold_piece, next_pieces, lines, level, drop_interval):
    panel_width = 160
    panel_x = WIDTH
    panel_rect = pygame.Rect(panel_x, 0, panel_width, HEIGHT)
    pygame.draw.rect(surface, SIDE_BG, panel_rect)

    font = pygame.font.Font(None, 26)
    small_font = pygame.font.Font(None, 22)

    y = 10

    text = font.render("HOLD", True, WHITE)
    surface.blit(text, (panel_x + 10, y))
    y += 25
    if hold_piece is not None:
        draw_mini_piece(surface, hold_piece["matrix"], hold_piece["color"], panel_x + 10, y)
    y += 90

    text = font.render("NEXT", True, WHITE)
    surface.blit(text, (panel_x + 10, y))
    y += 25

    for i, p in enumerate(next_pieces[:PIECE_QUEUE_SIZE]):
        draw_mini_piece(surface, p["matrix"], p["color"], panel_x + 10, y + i * 60)

    y = HEIGHT - 120

    text = font.render(f"Lineas: {lines}", True, WHITE)
    surface.blit(text, (panel_x + 10, y))
    y += 25
    text = font.render(f"Nivel: {level}", True, WHITE)
    surface.blit(text, (panel_x + 10, y))
    y += 25
    text = small_font.render(f"Vel: {drop_interval:.0f}ms", True, WHITE)
    surface.blit(text, (panel_x + 10, y))


def draw(screen, board, piece, hold_piece, next_pieces, score, level, drop_interval, game_over):
    screen.fill(BG)

    # Ghost piece
    ghost_y = get_ghost_y(board, piece)
    for py, row in enumerate(piece["matrix"]):
        for px, filled in enumerate(row):
            if filled and ghost_y + py >= 0:
                draw_cell(screen, piece["x"] + px, ghost_y + py, piece["color"], alpha=GHOST_ALPHA)

    # Board
    for y, row in enumerate(board):
        for x, color in enumerate(row):
            if color is not None:
                draw_cell(screen, x, y, color)
            else:
                pygame.draw.rect(screen, GRID, (x * CELL, y * CELL, CELL, CELL), 1)

    # Current piece
    for py, row in enumerate(piece["matrix"]):
        for px, filled in enumerate(row):
            if filled and piece["y"] + py >= 0:
                draw_cell(screen, piece["x"] + px, piece["y"] + py, piece["color"])

    # Side panel
    draw_side_panel(screen, hold_piece, next_pieces, score, level, drop_interval)

    # Game over overlay
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))
        message = pygame.font.Font(None, 46).render("GAME OVER", True, WHITE)
        hint = pygame.font.Font(None, 26).render("Pulsa R para reiniciar", True, WHITE)
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

    pygame.display.flip()


def main():
    total_width = WIDTH + 160
    screen = pygame.display.set_mode((total_width, HEIGHT))
    pygame.display.set_caption("Tetris RL")
    clock = pygame.time.Clock()

    board = make_board()
    bag = make_bag()
    queue = []

    def refill_queue():
        nonlocal bag, queue
        while len(queue) < PIECE_QUEUE_SIZE + 1:
            if not bag:
                bag = make_bag()
            idx = bag.pop()
            shape, color = SHAPES[idx]
            queue.append(new_piece_from_shape(shape, color))

    refill_queue()
    piece = queue.pop(0)
    refill_queue()

    hold_piece = None
    can_hold = True

    score = 0
    level = 1
    game_over = False

    start_time = time.time()
    last_drop_time = start_time
    drop_interval = 500

    running = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = make_board()
                    bag = make_bag()
                    queue = []
                    refill_queue()
                    piece = queue.pop(0)
                    refill_queue()
                    hold_piece = None
                    can_hold = True
                    score = 0
                    level = 1
                    game_over = False
                    start_time = time.time()
                    last_drop_time = start_time
                    drop_interval = 500

                if not game_over:
                    if event.key == pygame.K_a:
                        try_rotate_with_wall_kicks(board, piece, direction="180")
                    elif event.key == pygame.K_s:
                        try_rotate_with_wall_kicks(board, piece, direction="ccw")
                    elif event.key == pygame.K_d:
                        try_rotate_with_wall_kicks(board, piece, direction="cw")
                    elif event.key == pygame.K_LEFT and not collides(board, piece, dx=-1):
                        piece["x"] -= 1
                    elif event.key == pygame.K_RIGHT and not collides(board, piece, dx=1):
                        piece["x"] += 1
                    elif event.key == pygame.K_DOWN and not collides(board, piece, dy=1):
                        piece["y"] += 1
                    elif event.key == pygame.K_SPACE:
                        while not collides(board, piece, dy=1):
                            piece["y"] += 1
                    elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
                        if can_hold:
                            if hold_piece is None:
                                hold_piece = {
                                    "matrix": [row[:] for row in piece["matrix"]],
                                    "color": piece["color"],
                                }
                                piece = queue.pop(0)
                                refill_queue()
                            else:
                                temp = {
                                    "matrix": [row[:] for row in piece["matrix"]],
                                    "color": piece["color"],
                                }
                                piece = {
                                    "matrix": hold_piece["matrix"],
                                    "color": hold_piece["color"],
                                    "x": COLS // 2 - len(hold_piece["matrix"][0]) // 2,
                                    "y": 0,
                                }
                                hold_piece = temp
                            can_hold = False

        # Velocidad variable con el tiempo (más lenta la progresión)
        now = time.time()
        elapsed_ms = (now - start_time) * 1000
        elapsed_seconds = elapsed_ms / 1000

        # Velocidad máxima (80 ms) se alcanza a los ~3000 segundos (~50 minutos)
        drop_interval = max(80, 500 - int(elapsed_seconds / 3000) * 420)
        level = max(1, int(elapsed_seconds / 60) + 1)

        if not game_over:
            if (now - last_drop_time) * 1000 >= drop_interval:
                last_drop_time = now
                if not collides(board, piece, dy=1):
                    piece["y"] += 1
                else:
                    lock_piece(board, piece)
                    board, cleared = clear_lines(board)
                    score += cleared
                    can_hold = True
                    piece = queue.pop(0)
                    refill_queue()
                    if collides(board, piece):
                        game_over = True

        draw(screen, board, piece, hold_piece, queue, score, level, drop_interval, game_over)

    pygame.quit()


if __name__ == "__main__":
    main()