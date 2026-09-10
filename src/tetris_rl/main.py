from tetris_rl.tetris import Tetris

def main():
    mode = 1  # Modes: 0 (pygame), 1 (terminal), 2 (headless)

    game = Tetris()

    if mode == 0:
        from tetris_rl.runners.pygame_runner import run
    if mode == 1:
        from tetris_rl.runners.terminal_runner import run
    if mode == 2:
        from tetris_rl.runners.headless_runner import run
    
    run(game)


if __name__ == "__main__":
    main()