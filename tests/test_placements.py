import unittest

from tetris_rl.config import SHAPES
from tetris_rl.piece import Piece
from tetris_rl.tetris_env import TetrisENV


class PlacementTests(unittest.TestCase):
    def test_all_empty_board_targets(self):
        for kind, shape, color in SHAPES:
            for rotation in range(4):
                for column in range(10):
                    with self.subTest(kind=kind, rotation=rotation, column=column):
                        env = TetrisENV()
                        env.reset(seed=42)
                        piece = Piece(kind, [row[:] for row in shape], color)
                        piece.pos_x = (10 - len(shape[0])) // 2
                        piece.pos_y = -2
                        env.game.actual_piece = piece
                        oriented = [row[:] for row in shape]
                        if kind != 'O':
                            for _ in range(rotation):
                                oriented = [list(row) for row in zip(*oriented[::-1])]
                        cells = [(x, y) for y, row in enumerate(oriented)
                                 for x, value in enumerate(row) if value]
                        left = min(x for x, y in cells)
                        width = max(x for x, y in cells) - left + 1
                        valid = env._decode_perform_action(rotation * 10 + column)
                        self.assertEqual(valid, column + width <= 10)
                        self.assertEqual(env.game.pieces_locked, 1)
                        if valid:
                            bottom = max(y for x, y in cells)
                            expected = {(column + x - left, 19 + y - bottom)
                                        for x, y in cells}
                            actual = {(x, y) for y, row in enumerate(env.game.board)
                                      for x, value in enumerate(row) if value}
                            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
