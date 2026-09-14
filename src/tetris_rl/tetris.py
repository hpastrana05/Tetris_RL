import math
import random

from tetris_rl.tetris_actions import TetrisActions
from tetris_rl.config import *
from tetris_rl.piece import Piece

class Tetris:
    def __init__(self, fall_interval_ms=None, rng=None):
        self.rng = rng if rng is not None else random.Random()
        
        if fall_interval_ms is not None and (not math.isfinite(fall_interval_ms) or fall_interval_ms <= 0):
            raise ValueError("fall_interval_ms must be finite and positive")
        
        self.fixed_fall_interval_ms = fall_interval_ms
        self.board = []
        self.actual_piece = None
        self.next_pieces = []
        self.saved_piece = None
        self.can_save = True

        self.level = 0
        self.lines_cleared = 0
        self.points = 0
        self.game_over = False

        self.reset()

    def _generate_next_pieces(self):

        while len(self.next_pieces) <= GROUP_SIZE:
            indexes = list(range(len(SHAPES)))
            self.rng.shuffle(indexes)

            for index in indexes:
                kind, shape, color = SHAPES[index]

                self.next_pieces.append(
                    Piece(kind, [row[:] for row in shape], color)
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

        self.lines_cleared += lines_cleared
        self._calculate_level()

        self.board = new_board
        
    def _calculate_level(self):
        self.level = self.lines_cleared // LINES_PER_LEVEL

    def _lock_piece(self):
        # Check every block before writing, so top-out cannot partially lock a piece.
        for y, row in enumerate(self.actual_piece.shape):
            if any(row) and self.actual_piece.pos_y + y < 0:
                self.game_over = True
                return

        for y, row in enumerate(self.actual_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.actual_piece.pos_x + x
                    grid_y = self.actual_piece.pos_y + y
                    self.board[grid_y][grid_x] = 1

        self._check_line_clear()
        self.pieces_locked += 1
    
    def _take_next_piece(self):
        self.can_save = True
        self.actual_piece = self.next_pieces.pop(0)

        self.actual_piece.pos_y = -2
        self.actual_piece.pos_x = (NUM_COLS - len(self.actual_piece.shape[0]))//2

        self._generate_next_pieces()
        self._reset_timers()

    def reset(self):
        self.board = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
        self.next_pieces = []
        self._generate_next_pieces()
        self._take_next_piece()
        self.saved_piece = None

        self.level = 0
        self.lines_cleared = 0
        self.game_over = False
        self.points = 0
        self.pieces_locked = 0


    def _reset_timers(self):
        self.fall_elapsed = 0.0
        self.lock_elapsed = 0.0

    @property
    def fall_interval_ms(self):
        if self.fixed_fall_interval_ms is not None:
            return self.fixed_fall_interval_ms
        return max(MAX_VELOCITY, MIN_VELOCITY * 0.8 ** self.level)

    def is_grounded(self):
        probe = Piece(self.actual_piece.kind, self.actual_piece.shape, self.actual_piece.color)
        probe.pos_x = self.actual_piece.pos_x
        probe.pos_y = self.actual_piece.pos_y
        return not probe.shift_down(self.board)

    def advance_time(self, dt_ms):
    
        if not math.isfinite(dt_ms) or dt_ms < 0:
            raise ValueError("dt_ms must be finite and non-negative")
        if self.game_over:
            return

        # Accumulate ground contact across moves and rotations until locking.
        if self.is_grounded():
            self.lock_elapsed += dt_ms
            if self.lock_elapsed >= LOCK_DELAY:
                self._lock_piece()
                if not self.game_over:
                    self._take_next_piece()
            return

        # In the air, wait for the next one-row fall.
        self.fall_elapsed += dt_ms
        if self.fall_elapsed >= self.fall_interval_ms:
            self.fall_elapsed = 0.0
            self.actual_piece.shift_down(self.board)

    def step(self, action, dt_ms=0):
        """Apply an action, then advance time (e.g. dt_ms=50 for RL)."""
        if not math.isfinite(dt_ms) or dt_ms < 0:
            raise ValueError("dt_ms must be finite and non-negative")

        if self.game_over:
            return

        if self.is_grounded():
            previous_piece =self.actual_piece
            self.advance_time(dt_ms)

            if self.game_over or self.actual_piece is not previous_piece:
                return
            self._apply_action(action)

        else:        
            self._apply_action(action)
            self.advance_time(dt_ms)

    def _apply_action(self, action):
        if self.game_over:
            return

        if action == TetrisActions.MOVE_L:
            self.actual_piece.move_left(self.board)

        elif action == TetrisActions.MOVE_R:
            self.actual_piece.move_right(self.board)

        elif action == TetrisActions.MOVE_D:
            self.actual_piece.shift_down(self.board)


        elif action == TetrisActions.DROP:
            while self.actual_piece.shift_down(self.board):
                pass
            self._lock_piece()
            if not self.game_over:
                self._take_next_piece()

        elif action == TetrisActions.ROTATE_CW:
            self.actual_piece.rotate(1, self.board)

        elif action == TetrisActions.ROTATE_CCW:
            self.actual_piece.rotate(-1, self.board)

        elif action == TetrisActions.ROTATE_180:
            self.actual_piece.rotate(2, self.board)

        elif action == TetrisActions.SAVE_PIECE:
            if not self.can_save:
                return
            
            if self.saved_piece:
                self.actual_piece, self.saved_piece = self.saved_piece, self.actual_piece

                shape = next(shape for kind, shape, color in SHAPES if kind == self.saved_piece.kind)

                self.saved_piece.shape = [row[:] for row in shape]
                self.saved_piece.rotation = 0
                

                self.actual_piece.pos_y = -2
                self.actual_piece.pos_x = (NUM_COLS - len(self.actual_piece.shape[0]))//2

            else:
                self.saved_piece = self.actual_piece
                shape = next(shape for kind, shape, _ in SHAPES if kind == self.saved_piece.kind)
                
                self.saved_piece.shape = [row[:] for row in shape]
                self.saved_piece.rotation = 0

                self._take_next_piece()

            self.can_save = False
            self._reset_timers()
