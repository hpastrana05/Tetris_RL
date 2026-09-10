from tetris_rl.tetris_actions import TetrisActions
from tetris_rl.tetris import Tetris

def render(game):
    board = [
        ["#" if cell else "." for cell in row] 
        for row in game.board
    ]

    piece = game.actual_piece
    for y, row in enumerate(piece.shape):
        for x, col in enumerate(row):
            if col:
                px = piece.pos_x + x
                py = piece.pos_y + y
                if 0 <= py < len(board) and 0 <= px < len(board[0]):
                    board[py][px] = "@"
    
    print()
    for row in board:
        print(" ".join(row))
    print(f"Puntos: {game.points}")

def run(game: Tetris):
    actions = {
        "a": TetrisActions.MOVE_L,
        "d": TetrisActions.MOVE_R,
        "s": TetrisActions.MOVE_D,
        "x": TetrisActions.DROP,
        "e": TetrisActions.ROTATE_CW,
        "q": TetrisActions.ROTATE_CCW,
        "w": TetrisActions.ROTATE_180
    }

    while not game.game_over:
        render(game)
        command = input(
            f"a: Left | d: Right | s: Move down | x: drop | \n" +
             "e: rotate_r | q: rotate_l | w: rotate_180 | h: exit "
        ).strip().lower()

        if command == "h":
            return
        
        action = actions.get(command)
        if action is not None:
            game.step(action)
    
    render(game)
    print("End game")
