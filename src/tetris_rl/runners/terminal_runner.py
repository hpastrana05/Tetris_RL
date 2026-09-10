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
    }

    while not game.game_over:
        render(game)
        command = input(
            "a: Left | d: Right | s: Move down | x: drop | q: exit"
        ).strip().lower()

        if command == "q":
            return
        
        action = actions.get(command)
        if action is not None:
            game.step(action)
    
    render(game)
    print("End game")
