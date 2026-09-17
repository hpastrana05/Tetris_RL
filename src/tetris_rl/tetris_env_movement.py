import gymnasium as gym
import numpy as np
from gymnasium import spaces

from tetris_rl.config import *
from tetris_rl.tetris import Tetris
from tetris_rl.tetris_actions import TetrisActions as Actions

class TetrisENV(gym.Env):

    def __init__(self):
        self.game = Tetris(fall_interval_ms=500)

        self.actions = [
            Actions.MOVE_L,
            Actions.MOVE_R,
            Actions.MOVE_D,
            Actions.ROTATE_CW,
            Actions.ROTATE_CCW,
            Actions.ROTATE_180,
            Actions.SAVE_PIECE,
            Actions.DROP,
            Actions.NO_OP,
        ]

        self.action_space = spaces.Discrete(len(self.actions))

        self.observation_space = spaces.Dict({
            "board": spaces.MultiBinary((NUM_ROWS, NUM_COLS)),
            "piece": spaces.MultiBinary((4,4)),
            "position": spaces.Box(
                low= np.array([-4, -4], dtype=np.int32),
                high = np.array([NUM_COLS, NUM_ROWS], dtype=np.int32),
                dtype= np.int32,
            ),
            "piece_type": spaces.Discrete(7),
            "rotation": spaces.Discrete(4),
            "next_pieces": spaces.MultiDiscrete([7] * PIECE_QUEUE_SIZE),
            "saved_piece": spaces.Discrete(8),
            "can_save": spaces.Discrete(2),
            "timers": spaces.Box(
                low= 0,
                high=np.inf,
                shape=(2,),
                dtype=np.float32,
            )
        })

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        self.game.reset()
        self.steps = 0

        return self._get_obs(), {}

    def step(self, action):
        previous_lines = self.game.lines_cleared
        previous_height = self._board_height()
        previous_board = np.array(self.game.board, copy=True)

        self.game.step(self.actions[action], dt_ms=50)
        self.steps += 1

        reward = self.reward(previous_lines, previous_height, previous_board)

        terminated = self.game.game_over
        truncated = self.steps >=10_000

        return self._get_obs(), reward, terminated, truncated, {}

    def reward(self, prev_lines, prev_height, prev_board):
        lines = self.game.lines_cleared - prev_lines
        height_increase = self._board_height() - prev_height

        board_changed = not np.array_equal(prev_board, self.game.board)

        result = 0.0

        if board_changed or lines > 0:
            result += 10.0 * lines**2

            if height_increase <= 0:
                result += 1.0
            else:
                result -= float(height_increase**2)

        if self.game.game_over:
            result -= 20.0

        return result
        

    def _board_height(self):
        for y, row in enumerate(self.game.board):
            if any(row):
                return NUM_ROWS - y
        return 0       

    def _get_obs(self):
        game = self.game
        piece = game.actual_piece
        position = np.array([piece.pos_x, piece.pos_y], dtype=np.int32,)

        board = np.array(game.board, dtype=np.int8)

        piece_array = np.zeros((4, 4), dtype=np.int8)

        for y, row in enumerate(piece.shape):
            for x, col in enumerate(row):
                piece_array[y,x] = col

        piece_ids = {
            "I": 0, "O": 1, "T": 2, "S": 3,
            "Z": 4, "J": 5, "L": 6
        }

        next_pieces = np.array(
            [piece_ids[p.kind] for p in game.next_pieces[:PIECE_QUEUE_SIZE]]
        )

        saved_piece = 7
        if game.saved_piece is not None:
            saved_piece = piece_ids[game.saved_piece.kind]

        return {
            "board": board,
            "piece": piece_array,
            "position": position,
            "piece_type": piece_ids[piece.kind],
            "rotation": piece.rotation,
            "next_pieces": next_pieces,
            "saved_piece": saved_piece,
            "can_save": int(game.can_save),
            "timers": np.array([game.fall_elapsed, game.lock_elapsed], dtype=np.float32)
        }