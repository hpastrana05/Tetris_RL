import unittest

from stable_baselines3.common.env_checker import check_env
from tetris_rl.tetris_env import TetrisENV
from tetris_rl.piece import Piece


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
        _, reward, _, _, info = self.env.step(7)
        self.assertAlmostEqual(reward, 0.2)
        self.assertEqual(info['pieces_locked'], 1)

    def test_creating_holes_is_negative(self):
        self.env.game.board[-1][4] = 1
        self.piece('O', [[1, 1], [1, 1]], 4)
        _, reward, _, _, info = self.env.step(7)
        self.assertLess(reward, 0)
        self.assertEqual(info['holes'], 1)

    def test_line_clears_and_score(self):
        for lines, points in enumerate((100, 300, 500, 800), 1):
            with self.subTest(lines=lines):
                self.env.reset(seed=42)
                for row in self.env.game.board[-lines:]:
                    row[:] = [1] * 9 + [0]
                self.piece('I', [[1], [1], [1], [1]], 9)
                _, reward, _, _, info = self.env.step(7)
                self.assertEqual(info['lines'], lines)
                self.assertEqual(info['points'], points)
                self.assertEqual(info['pieces_locked'], 1)
                self.assertGreater(reward, 10 * lines)

    def test_wait_move_and_hold_have_no_bonus(self):
        for action in (8, 0, 6, 6):
            _, reward, _, _, info = self.env.step(action)
            self.assertEqual(reward, 0)
            self.assertEqual(info['pieces_locked'], 0)

    def test_gravity_lock_and_reset(self):
        self.piece('O', [[1, 1], [1, 1]], 4)
        self.env.game.actual_piece.pos_y = 18
        for _ in range(9):
            self.assertEqual(self.env.step(8)[1], 0)
        self.assertAlmostEqual(self.env.step(8)[1], 0.2)
        self.assertEqual(self.env.game.pieces_locked, 1)
        self.env.reset(seed=42)
        self.assertEqual(self.env.game.pieces_locked, 0)

    def test_top_out_has_no_placement_bonus(self):
        self.env.game.board[0] = [1] * 10
        self.piece('O', [[1, 1], [1, 1]], 4)
        _, reward, terminated, _, info = self.env.step(7)
        self.assertTrue(terminated)
        self.assertEqual(reward, -20)
        self.assertEqual(info['pieces_locked'], 0)

    def test_gym_compatibility(self):
        check_env(self.env)


if __name__ == '__main__':
    unittest.main()
