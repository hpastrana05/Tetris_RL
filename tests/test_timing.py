import unittest

from tetris_rl.tetris import Tetris
from tetris_rl.tetris_actions import TetrisActions as Action


class TimingTests(unittest.TestCase):
    def grounded_game(self):
        game = Tetris()
        while game.actual_piece.shift_down(game.board):
            pass
        return game

    def test_gravity_threshold_and_no_op(self):
        game = Tetris()
        y = game.actual_piece.pos_y
        for _ in range(9):
            game.step(Action.NO_OP, dt_ms=50)
        self.assertEqual(game.actual_piece.pos_y, y)
        game.step(Action.NO_OP, dt_ms=50)
        self.assertEqual(game.actual_piece.pos_y, y + 1)

    def test_soft_drop_and_lateral_action_do_not_reset_lock(self):
        game = self.grounded_game()
        piece = game.actual_piece
        game.step(Action.MOVE_D, dt_ms=250)
        game.step(Action.MOVE_L, dt_ms=249)
        self.assertIs(game.actual_piece, piece)
        game.advance_time(1)
        self.assertIsNot(game.actual_piece, piece)
        self.assertEqual(game.fall_elapsed, 0)
        self.assertEqual(game.lock_elapsed, 0)

    def test_drop_hold_and_reset_clear_timers(self):
        game = Tetris()
        for action in (Action.DROP, Action.SAVE_PIECE, Action.DROP, Action.SAVE_PIECE):
            game.advance_time(100)
            game.step(action)
            self.assertEqual(game.fall_elapsed, 0)
            self.assertEqual(game.lock_elapsed, 0)
        game.advance_time(100)
        game.reset()
        self.assertEqual(game.fall_elapsed, 0)
        self.assertEqual(game.lock_elapsed, 0)

    def test_long_frame_falls_only_one_row(self):
        game = Tetris()
        piece = game.actual_piece
        y = piece.pos_y
        game.advance_time(12000)
        self.assertIs(game.actual_piece, piece)
        self.assertEqual(piece.pos_y, y + 1)
        self.assertEqual(game.fall_elapsed, 0)

    def test_landing_starts_lock_on_next_update(self):
        game = self.grounded_game()
        piece = game.actual_piece
        piece.pos_y -= 1
        game.advance_time(500)
        self.assertTrue(game.is_grounded())
        self.assertEqual(game.lock_elapsed, 0)
        game.advance_time(499)
        self.assertIs(game.actual_piece, piece)
        game.advance_time(1)
        self.assertIsNot(game.actual_piece, piece)

    def test_leaving_ground_resets_lock(self):
        game = Tetris()
        from tetris_rl.piece import Piece
        game.actual_piece = Piece('O', [[1, 1], [1, 1]], None)
        game.actual_piece.pos_x = 3
        game.actual_piece.pos_y = 16
        game.board[18][3] = 1
        game.advance_time(200)
        self.assertEqual(game.lock_elapsed, 200)
        game.step(Action.MOVE_R)
        self.assertEqual(game.lock_elapsed, 0)

    def test_fixed_speed_and_validation(self):
        game = Tetris(fall_interval_ms=500)
        game.level = 20
        self.assertEqual(game.fall_interval_ms, 500)
        for dt in (-1, float('inf'), float('nan')):
            with self.assertRaises(ValueError):
                game.advance_time(dt)
        game.game_over = True
        y = game.actual_piece.pos_y
        game.step(Action.NO_OP, dt_ms=500)
        self.assertEqual(game.actual_piece.pos_y, y)


if __name__ == '__main__':
    unittest.main()
