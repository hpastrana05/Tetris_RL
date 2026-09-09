import random

from tetris_rl.config import *
from tetris_rl.piece import Piece

class Tetris:
    def __init__(self):
        self.board = []
        self.actual_piece = None
        self.next_pieces = []
        self.saved_piece = None

        self.reset()

    def _generate_next_pieces(self):
        next_indexes = list(range(len(SHAPES)))
        random.shuffle(next_indexes)
        next_pieces = []

        # only generate new pieces if the next_pieces list is empty or has reached the group size
        if len(self.next_pieces) in [0, GROUP_SIZE]:

            for i in range(GROUP_SIZE):
                next_pieces.append(Piece(SHAPES[next_indexes[i]][0], SHAPES[next_indexes[i]][1]))

        return next_pieces
    
    def reset(self):
        self.board = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
        self.next_pieces = self._generate_next_pieces()
        self.actual_piece = self.next_pieces.pop(0)
        self.saved_piece = Piece([], (0, 0, 0))


    def step(self, action):
        pass
