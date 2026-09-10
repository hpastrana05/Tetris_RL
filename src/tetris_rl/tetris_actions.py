from enum import Enum, auto

class TetrisActions(Enum):
    MOVE_L = auto()
    MOVE_R = auto()
    MOVE_D = auto()
    DROP = auto()
    ROTATE_CW = auto()
    ROTATE_CCW = auto()
    ROTATE_180 = auto()
    SAVE_PIECE = auto()
    
