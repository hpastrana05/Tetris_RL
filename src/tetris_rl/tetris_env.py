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

        self.game.rng = self.np_random
        self.game.reset()
        self.steps = 0

        return self._get_obs(), {}

    def step(self, action):
        previous_lines = self.game.lines_cleared
        previous_metrics = self._board_metrics()
        previous_pieces = self.game.pieces_locked

        self.game.step(self.actions[int(action)], dt_ms=50)
        self.steps += 1

        reward = self.reward(previous_lines, previous_metrics, previous_pieces)

        terminated = self.game.game_over
        truncated = self.steps >=10_000

        info = {
            "lines": self.game.lines_cleared,
            "holes": self._board_metrics()[1],
            "points": self.game.points,
            "pieces_locked": self.game.pieces_locked,
        }

        
        return self._get_obs(), reward, terminated, truncated, info

    def reward(self, prev_lines, prev_metrics, prev_pieces):
        lines = self.game.lines_cleared - prev_lines

        height, holes, bumpiness = self._board_metrics()
        prev_height, prev_holes, prev_bumpiness = prev_metrics

        result = (
            10.0 * lines
            + 1.0 * (self.game.pieces_locked - prev_pieces)
            - 0.1 * (height - prev_height)
            - 2.0 * (holes - prev_holes)
            - 0.1 * (bumpiness - prev_bumpiness)
        )

        if self.game.game_over:
            result -= 20

        return result
        

    def _board_metrics(self):
        board = np.asarray(self.game.board, dtype=bool)
        occupied = board.any(axis=0)

        heights = np.where(
            occupied,
            board.shape[0] - board.argmax(axis=0),
            0,
        )

        holes = np.sum(
            np.maximum.accumulate(board, axis=0) & ~board
        )

        aggregate_height = heights.sum()
        bumpiness = np.abs(np.diff(heights)).sum()

        return float(aggregate_height), float(holes), float(bumpiness)


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
