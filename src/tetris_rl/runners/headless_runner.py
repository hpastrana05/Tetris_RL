from tetris_rl.tetris_actions import TetrisActions

def run(game):
    steps = 0
    
    while not game.game_over and steps < 10_000:
        game.step(TetrisActions.DROP)
        steps += 1

    print(f"Puntos: {game.points} | Pasos: {steps}")        
