import unittest

from stable_baselines3.common.env_checker import check_env
from tetris_rl.tetris_env import TetrisENV
from tetris_rl.piece import Piece
from tetris_rl.tetris_actions import TetrisActions as Actions


class RewardTests(unittest.TestCase):
    def setUp(self):
        self.env = TetrisENV()
        self.env.reset(seed=42)

    def piece(self, kind, shape, x):
        p = Piece(kind, shape, (0, 0, 0))
        p.pos_x, p.pos_y = x, -4
        self.env.game.actual_piece = p

    def test_clean_placement_is_positive(self):
        self.piece('O', [[1, 1], [1, 1]], 4)
        _, reward, _, _, info = self.env.step(4)
        self.assertAlmostEqual(reward, 0.2)
        self.assertEqual(info['pieces_locked'], 1)

    def test_creating_holes_is_negative(self):
        self.env.game.board[-1][4] = 1
        self.piece('O', [[1, 1], [1, 1]], 4)
        _, reward, _, _, info = self.env.step(4)
        self.assertLess(reward, 0)
        self.assertEqual(info['holes'], 1)

    def test_line_clears_and_score(self):
        for lines, points in enumerate((100, 300, 500, 800), 1):
            with self.subTest(lines=lines):
                self.env.reset(seed=42)
                for row in self.env.game.board[-lines:]:
                    row[:] = [1] * 9 + [0]
                self.piece('I', [[1], [1], [1], [1]], 9)
                _, reward, _, _, info = self.env.step(9)
                self.assertEqual(info['lines'], lines)
                self.assertEqual(info['points'], points)
                self.assertEqual(info['pieces_locked'], 1)
                self.assertGreater(reward, 10 * lines)

    def primitive_reward(self, action):
        # Internal motor actions still have no placement bonus until locking.
        previous = (self.env.game.lines_cleared, self.env._board_metrics(),
                    self.env.game.pieces_locked)
        self.env.game.step(action, dt_ms=50)
        return self.env.reward(*previous)

    def test_wait_move_and_hold_have_no_bonus(self):
        for action in (Actions.NO_OP, Actions.MOVE_L,
                       Actions.SAVE_PIECE, Actions.SAVE_PIECE):
            self.assertEqual(self.primitive_reward(action), 0)
            self.assertEqual(self.env.game.pieces_locked, 0)

    def test_gravity_lock_and_reset(self):
        self.piece('O', [[1, 1], [1, 1]], 4)
        self.env.game.actual_piece.pos_y = 18
        for _ in range(9):
            self.assertEqual(self.primitive_reward(Actions.NO_OP), 0)
        self.assertAlmostEqual(self.primitive_reward(Actions.NO_OP), 0.2)
        self.assertEqual(self.env.game.pieces_locked, 1)
        self.env.reset(seed=42)
        self.assertEqual(self.env.game.pieces_locked, 0)

    def test_top_out_has_no_placement_bonus(self):
        self.env.game.board[0] = [1] * 10
        self.piece('O', [[1, 1], [1, 1]], 4)
        _, reward, terminated, _, info = self.env.step(4)
        self.assertTrue(terminated)
        self.assertEqual(reward, -20)
        self.assertEqual(info['pieces_locked'], 0)

    def test_gym_compatibility(self):
        check_env(self.env)


if __name__ == '__main__':
    unittest.main()
