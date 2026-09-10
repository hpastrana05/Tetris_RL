

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.pos_x = 0
        self.pos_y = 0

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
