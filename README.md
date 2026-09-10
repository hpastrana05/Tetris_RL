# Tetris_RL
Create a Tetris game and make a RL algorithm to teach it how to play

## Architecture

The approach that I followed is to have a class Tetris which will control the logic of the game without any kind of drawing. This allows to run the game in 3 different ways.

1. **headless:** This way is not showing any state of the game just running and returning the points and steps
2. **terminal:** This way shows the state of the game via terminal
3. **pygame:** Uses the pygame library to show the game in a better way


## Running

After running the code, to select the way of running is to cahnge the `mode` variable in `main.py`

`uv run tetris-rl `