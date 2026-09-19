from pathlib import Path

from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor

from tetris_rl.tetris_env import TetrisENV
from tetris_rl.tetris_env_movement import TetrisENVMov

model_path = "models/tetris_dqn_piece_placement"

env = TetrisENV()


# Checks compatibility with library 
check_env(env)

# Monitors the duration and rewards of steps
env = Monitor(env)

model = DQN(
    "MultiInputPolicy",
    env,
    buffer_size = 100_000,
    learning_starts = 10_000,
    exploration_fraction = 0.05,
    verbose = 1,
    device="cuda" # "cuda" for gpu / "cpu" for cpu
)

model.learn(total_timesteps=1_000_000)
Path(model_path).parent.mkdir(parents=True, exist_ok=True)
model.save(model_path)

env.close()
