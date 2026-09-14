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

## Training

In train.py, there is a file where the training of the model is done

`uv run python -m tetris_rl.train`


## Simulation time and RL

The game owns gravity and the continuous ground-contact lock delay. Pygame
advances it using elapsed frame time. Headless training can advance simulated
time without sleeping:

```python
from tetris_rl.tetris import Tetris
from tetris_rl.tetris_actions import TetrisActions

game = Tetris(fall_interval_ms=500)  # Optional fixed speed for initial training.
game.step(TetrisActions.MOVE_L, dt_ms=50)
game.step(TetrisActions.NO_OP, dt_ms=50)  # Wait while simulation time advances.
```

Without `fall_interval_ms`, gravity accelerates with the level. `step(action)`
only applies input; `advance_time(dt_ms)` advances time separately. Use either
`step(action, dt_ms=50)` or `step(action)` followed by `advance_time(50)`, avoiding
double-counting time. Soft drop respects `LOCK_DELAY`; hard drop locks immediately.
Each update performs at most one automatic fall and discards excess fall time.
Lock time starts accumulating on the update after landing. New pieces start with
fresh timers; excess time after locking is discarded. Use small time steps such
as 50 ms for training; long frames do not catch up on missed falls.
The terminal runner advances 50 ms per recognized command (Enter waits).

A future Gymnasium observation should include `fall_elapsed`, `lock_elapsed`,
`fall_interval_ms`, and `level`, alongside the board and piece state, so the agent
can distinguish states with different times until gravity or locking.

Run timing checks with `uv run python -m unittest discover -s tests -v`.
