import gymnasium as gym
import numpy as np
from gymnasium import spaces
from copy import deepcopy

from tetris_rl.config import *
from tetris_rl.tetris import Tetris
from tetris_rl.tetris_actions import TetrisActions as Actions

SCORE_SCALE = 100.0
HOLE_WEIGHT = 0.2
GAME_OVER_PENALTY = 10.0
NOT_VALID_PENALTY = 0.05

NUM_NEXT_OBS = 2

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

        self.action_space = spaces.Discrete(40)

        self.observation_space = spaces.Dict({
            "board": spaces.MultiBinary((NUM_ROWS, NUM_COLS)),
            "piece": spaces.Discrete(7),
            "next_pieces": spaces.MultiDiscrete([7] * NUM_NEXT_OBS), 
            
        })

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        self.game.rng = self.np_random
        self.game.reset()
        self.steps = 0

        return self._get_obs(), {}

    def step(self, action):
        prev_points = self.game.points
        prev_holes = self._board_metrics()[1]
        
        valid = self._decode_perform_action(action)
        self.steps += 1

        reward = self.reward(prev_points, prev_holes)

        if not valid:
            reward -= NOT_VALID_PENALTY

        terminated = self.game.game_over
        truncated = self.steps >=10_000

        info = {
            "lines": self.game.lines_cleared,
            "holes": self._board_metrics()[1],
            "points": self.game.points,
            "pieces_locked": self.game.pieces_locked,
            "invalid_action": not valid
        }

        
        return self._get_obs(), reward, terminated, truncated, info

    def reward(self, prev_points, prev_holes):
        points_gained = self.game.points - prev_points
        current_holes = self._board_metrics()[1]

        hole_change = current_holes - prev_holes

        result = (
            points_gained / SCORE_SCALE
            - HOLE_WEIGHT * hole_change
        )

        if self.game.game_over:
            result -= GAME_OVER_PENALTY
    
        return result
    
    def action_masks(self):
        mask = np.zeros(self.action_space.n)

        for action in range(self.action_space.n):
            trial = deepcopy(self.game)
            mask[action] = self._perform_decoded_action(trial, action)
        
        return mask


    def _perform_decoded_action(self, game, action):
        rotation = action // 10
        position = action % 10

        if game.actual_piece.kind !=  "O":
            turns = (rotation - game.actual_piece.rotation) % 4

            rotation_action = {
                1: Actions.ROTATE_CW,
                2: Actions.ROTATE_180,
                3: Actions.ROTATE_CCW,
            }.get(turns)

            if rotation_action is not None:
                if game.step(rotation_action) is False:
                    return False
            
            if game.actual_piece.rotation != rotation:
                return False
            
        piece = game.actual_piece

        left_offset = min(
            x
            for row in piece.shape
            for x, cell in enumerate(row)
            if cell
        )

        current_column = piece.pos_x + left_offset
        displacement = position - current_column

        if displacement != 0:
            move = Actions.MOVE_R if displacement > 0 else Actions.MOVE_L

            for _ in range(abs(displacement)):
                previous_x = game.actual_piece.pos_x
                result = game.step(move)

                if result is False or game.actual_piece.pos_x == previous_x:
                    return False
                
        
        game.step(Actions.DROP)

        return True


    def _is_valid_action(self, action):
        if not self.action_space.contains(action):
            return False
        
        trial = deepcopy(self.game)
        return self._perform_decoded_action(trial, action)

        
    def _decode_perform_action(self, action):
        if not self.action_space.contains(action):
            raise ValueError(f"Action not in defined space: {action}")

        trial = deepcopy(self.game)
        valid = self._perform_decoded_action(trial, action)

        if not valid:
            return False
        
        self._perform_decoded_action(self.game, action)
        return True


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

        next_pieces = []
        for piece in self.game.next_pieces[:NUM_NEXT_OBS]:
            next_pieces.append(PIECE_IDS[piece.kind])

        return {
            "board": np.asarray(self.game.board, dtype=np.int8),
            "piece": PIECE_IDS[self.game.actual_piece.kind],
            "next_pieces": np.asarray(next_pieces)
        }