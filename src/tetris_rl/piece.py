from tetris_rl.rotation import (
    KICKS_NORMAL,
    KICKS_I,
    KICKS_180_NORMAL,
    KICKS_180_I
)

class Piece:
    def __init__(self, kind, shape, color):
        self.kind = kind
        self.shape = shape
        self.color = color
        self.pos_x = 0
        self.pos_y = 0
        self.rotation = 0

    def _try_move(self, dx, dy, grid):
        self.pos_x += dx
        self.pos_y += dy

        if self._check_collision(grid):
            self.pos_x -= dx
            self.pos_y -= dy
            return False
        return True


    def _check_collision(self, grid):
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

    def move_left(self, board):
        self._try_move(-1, 0, board)

    def move_right(self, board):
        self._try_move(1, 0, board)

    def shift_down(self, board):
        return self._try_move(0, 1, board)

    def rotate(self, turns, board):
        if turns not in (1, -1, 2):
            raise ValueError("turns debe ser 1, -1 o 2")
        
        if self.kind == "O":
            return False
        
        old_shape = self.shape
        old_x = self.pos_x
        old_y = self.pos_y
        old_rotation = self.rotation

        new_rotation = (old_rotation + turns) % 4

        if turns == 1:
            rotated = [list(row) for row in zip(*old_shape[::-1])]
        elif turns == -1:
            rotated = [list(row) for row in zip(*old_shape)][::-1]
        else:
            rotated = [row[::-1] for row in old_shape[::-1]]
        
        if turns == 2:
            table = KICKS_180_I if self.kind == "I" else KICKS_180_NORMAL
        else:
            table = KICKS_I if self.kind == "I" else KICKS_NORMAL

        self.shape = rotated

        for dx, dy in table[(old_rotation, new_rotation)]:
            self.pos_x = old_x + dx
            self.pos_y = old_y + dy

            if not self._check_collision(board):
                self.rotation = new_rotation
                return True

        self.shape = old_shape
        self.pos_x = old_x
        self.pos_y = old_y
        return False
