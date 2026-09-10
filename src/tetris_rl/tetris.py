import random

from tetris_rl.tetris_actions import TetrisActions
from tetris_rl.config import *
from tetris_rl.piece import Piece

class Tetris:
    def __init__(self):
        self.board = []
        self.actual_piece = None
        self.next_pieces = []
        self.saved_piece = None

        self.points = 0
        self.game_over = False

        self.reset()

    def _generate_next_pieces(self):
      while len(self.next_pieces) <= GROUP_SIZE:
          indexes = list(range(len(SHAPES)))
          random.shuffle(indexes)

          for index in indexes:
              shape, color = SHAPES[index]

              self.next_pieces.append(
                  Piece([row[:] for row in shape], color)
              )

    def _calculate_points(self, lines):
        points_by_lines = (0, 100, 300, 500, 800)
        self.points += points_by_lines[lines]

    
    def _check_line_clear(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = NUM_ROWS - len(new_board)

        self._calculate_points(lines_cleared)
        
        while len(new_board) < NUM_ROWS:
            new_board.insert(0, [0 for _ in range(NUM_COLS)])

        self.board = new_board

    def _lock_piece(self):
        for y, row in enumerate(self.actual_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.actual_piece.pos_x + x
                    grid_y = self.actual_piece.pos_y + y
                    self.board[grid_y][grid_x] = 1

        self._check_line_clear()
    
    def _take_next_piece(self):
        self.actual_piece = self.next_pieces.pop(0)

        self.actual_piece.pos_y = 0
        self.actual_piece.pos_x = (NUM_COLS - len(self.actual_piece.shape[0]))//2

        self._generate_next_pieces()

        self.game_over = self.actual_piece._check_collision(self.board)

    def reset(self):
        self.board = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
        self.next_pieces = []
        self._generate_next_pieces()
        self._take_next_piece()
        self.saved_piece = Piece([], (0, 0, 0))

        self.game_over = False
        self.points = 0


    def step(self, action):
        if self.game_over:
            return

        if action == TetrisActions.MOVE_L:
            self.actual_piece.move_left(self.board)

        elif action == TetrisActions.MOVE_R:
            self.actual_piece.move_right(self.board)

        elif action == TetrisActions.MOVE_D:
            if not self.actual_piece.shift_down(self.board):
                self._lock_piece()
                self._take_next_piece()


        elif action == TetrisActions.DROP:
            while self.actual_piece.shift_down(self.board):
                pass
            self._lock_piece()
            self._take_next_piece()

        elif action == TetrisActions.ROTATE_CW:

            pass

        elif action == TetrisActions.ROTATE_CCW:
            pass

        elif action == TetrisActions.ROTATE_180:
            pass

        elif action == TetrisActions.SAVE_PIECE:
            pass
